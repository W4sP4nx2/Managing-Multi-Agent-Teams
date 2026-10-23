"""Distribution invariants and grader sabotage that must hold before kernel tests."""
from __future__ import annotations

import ast
import json
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace

import pytest

from tests.workshop_support import prepared_notebook, workshop_paths
from tools.build_core_notebooks import CORE_FILENAMES, build

pytestmark = pytest.mark.unit


def test_canonical_handouts_match_sources_and_contain_no_live_branch(repo_root):
    assert {path.name for path in (repo_root / "notebooks").iterdir()} == set(CORE_FILENAMES)
    build(check=True)
    for path in workshop_paths(repo_root).values():
        notebook = json.loads(path.read_text(encoding="utf-8"))
        flag_assignments = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            tree = ast.parse("".join(cell["source"]))
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                    assert not any(name.split(".")[0] in {"openai", "instructor", "anthropic"} for name in imports), path
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    assert not node.func.attr.startswith("kickoff"), path
                if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "USE_LIVE_LLM"
                                                        for target in node.targets):
                    flag_assignments.append(node.value)
                if isinstance(node, ast.If):
                    assert not any(isinstance(child, ast.Name) and child.id == "USE_LIVE_LLM"
                                   for child in ast.walk(node.test)), path
        assert flag_assignments, path
        assert all(isinstance(node, ast.Constant) and node.value is False for node in flag_assignments), path


def lab1_score(repo_root, replacement: str) -> int:
    notebook = prepared_notebook(workshop_paths(repo_root)["lab1"], "lab1", "fixed")
    state = {}
    with redirect_stdout(StringIO()):
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = replacement if cell["id"] == "lab1-learner-workspace" else "".join(cell["source"])
                exec(source, state)
    return state["lab1_score"]


@pytest.mark.parametrize("replacement,expected", [
    # A reject-everything validator must never receive points for blocking bad input.
    ('''from pydantic import BaseModel, ConfigDict, Field, model_validator
class StrictResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    findings: list[str]
    @model_validator(mode="before")
    @classmethod
    def reject_all(cls, value):
        raise ValueError("blocked")
''', 0),
    # An upper bound alone leaves the lower-range hole; only the extra-field gate earns credit.
    ('''from pydantic import BaseModel, ConfigDict, Field
class StrictResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str
    confidence_score: float = Field(le=1.0)
    findings: list[str]
''', 10),
    # Defaulting a required field silently weakens the contract; both gates depend on its shape.
    ('''from pydantic import BaseModel, ConfigDict, Field
class StrictResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = "default topic"
    confidence_score: float = Field(ge=0.0, le=1.0)
    findings: list[str]
''', 0),
])
def test_lab1_sabotage_cannot_fake_a_full_contract(repo_root, replacement, expected):
    assert lab1_score(repo_root, replacement) == expected


def test_lab2_extra_manager_tool_does_not_pass_separation_of_duties(repo_root):
    notebook = json.loads(workshop_paths(repo_root)["lab2"].read_text())
    grader = next(cell for cell in notebook["cells"] if cell.get("id") == "84aaa3ad")
    architect = object()
    manager = SimpleNamespace(tools=[SimpleNamespace(name="approve_code_tool"),
                                     SimpleNamespace(name="run_tests_tool")], allow_delegation=True)
    state = {"manager_agent": manager, "architect_task": architect,
             "coder_task": SimpleNamespace(context=[architect])}
    with redirect_stdout(StringIO()):
        exec("".join(grader["source"]), state)
    assert state["manager_sod_ok"] is False
    assert state["lab2_score"] == 10
