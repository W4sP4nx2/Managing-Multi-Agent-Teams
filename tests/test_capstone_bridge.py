"""Historical demo links must never restore paid execution, even with credentials."""
import builtins
import json

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("forced_legacy_flag", [False, True])
def test_historical_demo_has_no_provider_path(repo_root, monkeypatch, capsys, forced_legacy_flag):
    notebook = json.loads((repo_root / "extensions/bonus_live_demo.ipynb").read_text())
    code = {cell["id"]: "".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code"}
    monkeypatch.setenv("OPENAI_API_KEY", "unused-synthetic-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "unused-synthetic-key")
    original = builtins.__import__
    def refuse_provider(name, *args, **kwargs):
        if name.split(".")[0] in {"openai", "anthropic", "instructor"}:
            raise AssertionError("Compatibility notebook attempted a provider import")
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", refuse_provider)
    namespace = {}
    exec(code["bonus-config"], namespace)
    namespace["USE_LIVE_LLM"] = forced_legacy_flag
    exec(code["bonus-live-call"], namespace)
    output = capsys.readouterr().out
    assert "Actual API cost: $0.00" in output and "live_simulation_orchestrator.py" in output
    assert "client" not in namespace and "result" not in namespace
