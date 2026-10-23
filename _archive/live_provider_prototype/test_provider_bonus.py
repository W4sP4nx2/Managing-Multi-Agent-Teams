"""Execute the separate bonus demo's actual cells with an entirely local fake SDK."""
from __future__ import annotations

import builtins
import contextlib
import io
import json
import sys
from types import ModuleType, SimpleNamespace

import pytest
from pydantic import ValidationError

pytestmark = pytest.mark.integration


def bonus_code(repo_root):
    notebook = json.loads((repo_root / "extensions/bonus_live_demo.ipynb").read_text())
    return {cell["id"]: compile("".join(cell["source"]), cell["id"], "exec", dont_inherit=True)
            for cell in notebook["cells"] if cell["cell_type"] == "code"}


def test_disabled_bonus_needs_neither_provider_import_nor_api_key(repo_root, monkeypatch):
    code = bonus_code(repo_root)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    original_import = builtins.__import__

    def deny_provider(name, *args, **kwargs):
        if name.split(".")[0] == "openai":
            raise AssertionError("Disabled bonus tried to import the provider SDK")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", deny_provider)
    ns = {"__name__": "bonus_disabled"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(code["bonus-config"], ns)
        exec(code["bonus-live-call"], ns)
    assert ns["USE_LIVE_LLM"] is False
    assert "client" not in ns and "result" not in ns


def test_enabled_bonus_checks_api_key_before_importing_provider(repo_root, monkeypatch):
    code = bonus_code(repo_root)
    ns = {"__name__": "bonus_no_key"}
    exec(code["bonus-config"], ns)
    ns["USE_LIVE_LLM"] = True
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setitem(sys.modules, "openai", None)
    with pytest.raises(RuntimeError, match="Set OPENAI_API_KEY"):
        exec(code["bonus-live-call"], ns)
    assert "client" not in ns


@pytest.mark.parametrize("output_state", ["valid", "missing", "invalid_schema", "provider_error"])
def test_enabled_bonus_uses_typed_sdk_result_and_surfaces_failures(repo_root, monkeypatch, output_state):
    code = bonus_code(repo_root)
    ns = {"__name__": "bonus_fake_sdk"}
    exec(code["bonus-config"], ns)
    ns["USE_LIVE_LLM"] = True
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "synthetic-test-model")
    calls = []

    def parse(**kwargs):
        calls.append(kwargs)
        if output_state == "provider_error":
            raise RuntimeError("Synthetic provider failure")
        result = None
        if output_state != "missing":
            result = kwargs["response_format"].model_validate({
                "topic": "API Security", "confidence_score": 150.5 if output_state == "invalid_schema" else 0.95,
                "findings": ["Use HTTPS", "Limit API permissions"],
            })
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(parsed=result))])

    fake_sdk = ModuleType("openai")
    fake_sdk.OpenAI = lambda: SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(parse=parse)))
    monkeypatch.setitem(sys.modules, "openai", fake_sdk)
    with contextlib.redirect_stdout(io.StringIO()):
        if output_state == "valid":
            exec(code["bonus-live-call"], ns)
        else:
            expected_error = ValidationError if output_state == "invalid_schema" else RuntimeError
            with pytest.raises(expected_error):
                exec(code["bonus-live-call"], ns)
    assert len(calls) == 1
    assert calls[0]["model"] == "synthetic-test-model"
    assert calls[0]["response_format"] is ns["ResearchOutput"]
    assert calls[0]["messages"][0]["role"] == "user"
    if output_state == "valid":
        assert isinstance(ns["result"], ns["ResearchOutput"])
        assert ns["result"].confidence_score == 0.95
