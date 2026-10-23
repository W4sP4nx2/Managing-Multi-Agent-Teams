"""Exercise the actual handout DX helpers without constructing live agent teams."""
from __future__ import annotations

import json
from datetime import date

import pytest
from pydantic import BaseModel, Field, field_validator, model_validator

from tests.workshop_support import notebook_definitions, workshop_paths

pytestmark = pytest.mark.unit


@pytest.fixture(params=["lab2", "lab3", "capstone"])
def inspector(repo_root, request):
    path = workshop_paths(repo_root)[request.param]
    with notebook_definitions(path, request.param, {"inspect_state", "safe_validate"}) as namespace:
        # The pure-definition loader deliberately omits general library imports.
        namespace["json"] = json
        yield namespace


def test_valid_contract_returns_typed_model(inspector, capsys):
    class Contract(BaseModel):
        user_id: str = Field(strict=True)

    result = inspector["safe_validate"](Contract, {"user_id": "101"})
    assert isinstance(result, Contract)
    assert result.user_id == "101"
    assert capsys.readouterr().out == ""


def test_invalid_field_returns_none_with_readable_path(inspector, capsys):
    class Entry(BaseModel):
        user_id: str = Field(strict=True)

    class Contract(BaseModel):
        entries: list[Entry]

    result = inspector["safe_validate"](Contract, {"entries": [{"user_id": 101}]})
    output = capsys.readouterr().out
    assert result is None
    assert "GOVERNANCE BLOCK at Contract" in output
    assert "Field: entries.0.user_id" in output
    assert "Input should be a valid string" in output
    assert "Traceback" not in output


def test_model_level_rejection_has_no_index_error_or_secret_echo(inspector, capsys):
    secret = "synthetic-secret-must-not-appear"

    class Contract(BaseModel):
        secret: str

        @model_validator(mode="before")
        @classmethod
        def reject_candidate(cls, value):
            raise ValueError("Policy requires successful QA")

    assert inspector["safe_validate"](Contract, {"secret": secret}) is None
    output = capsys.readouterr().out
    assert "Field: <model>" in output
    assert "Policy requires successful QA" in output
    assert secret not in output


def test_fixed_policy_message_does_not_echo_rejected_input(inspector, capsys):
    secret = "another-synthetic-secret"

    class Contract(BaseModel):
        user_id: str

        @field_validator("user_id")
        @classmethod
        def reject_id(cls, value):
            raise ValueError("user_id must be numeric and at most 12 digits")

    assert inspector["safe_validate"](Contract, {"user_id": secret}) is None
    output = capsys.readouterr().out
    assert "Field: user_id" in output
    assert "user_id must be numeric and at most 12 digits" in output
    assert secret not in output


@pytest.mark.parametrize("error_type", [RuntimeError, TypeError, ValueError])
def test_unexpected_errors_propagate(inspector, error_type):
    class BrokenSchema:
        @classmethod
        def model_validate(cls, value):
            raise error_type("unexpected validation implementation failure")

    with pytest.raises(error_type, match="unexpected validation implementation failure"):
        inspector["safe_validate"](BrokenSchema, {})


def test_inspector_renders_readable_json_and_non_json_fixture_values(inspector, capsys):
    inspector["inspect_state"]("fixture", {"user_id": "101", "date": date(2026, 10, 20)})
    output = capsys.readouterr().out
    body = output.split("INSPECTING: fixture\n", 1)[1].rsplit("\n" + "─" * 40, 1)[0]
    assert json.loads(body) == {"user_id": "101", "date": "2026-10-20"}
    assert '\n  "user_id": "101"' in body
