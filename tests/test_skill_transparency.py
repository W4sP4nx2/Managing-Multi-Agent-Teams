"""Inspect the actual Lab 2 source without invoking agents, tools, or a model."""
from __future__ import annotations

import ast
from contextlib import redirect_stdout
from io import StringIO
import json
from types import SimpleNamespace

import pytest

from tests.workshop_support import prepared_notebook
from tools.build_core_notebooks import notebook_from_source

pytestmark = pytest.mark.unit


class TrapTool:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.calls = 0

    def run(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("Skill transparency must never execute a tool")

    __call__ = run


@pytest.fixture
def source_notebook(repo_root):
    return notebook_from_source(repo_root / "tools/notebook_sources/02_lab_crewai.py")


def _cell(notebook, identifier):
    return next(cell for cell in notebook["cells"] if cell["id"] == identifier)


def _source(cell):
    return "".join(cell["source"])


def _agents_from_configuration(notebook):
    """Read the real tool docstrings and Agent keyword values as data only."""
    tree = ast.parse(_source(_cell(notebook, "88df3214")))
    tools = {node.name: TrapTool(node.name, ast.get_docstring(node))
             for node in tree.body if isinstance(node, ast.FunctionDef)
             and any(isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name)
                     and decorator.func.id == "tool" for decorator in node.decorator_list)}
    agents = {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name) and node.value.func.id == "Agent"):
            continue
        keywords = {keyword.arg: keyword.value for keyword in node.value.keywords}
        agents[node.targets[0].id] = SimpleNamespace(
            role=ast.literal_eval(keywords["role"]),
            tools=[tools[name.id] for name in keywords["tools"].elts],
            allow_delegation=ast.literal_eval(keywords["allow_delegation"]),
        )
    return agents, tools


def _inspect(notebook):
    agents, tools = _agents_from_configuration(notebook)
    original_lists = {name: list(agent.tools) for name, agent in agents.items()}
    original_list_objects = {name: agent.tools for name, agent in agents.items()}
    namespace = dict(agents)
    output = StringIO()
    with redirect_stdout(output):
        exec(_source(_cell(notebook, "lab2-skill-transparency")), namespace)
    for name, agent in agents.items():
        assert agent.tools is original_list_objects[name]
        assert agent.tools == original_lists[name]
    assert all(tool.calls == 0 for tool in tools.values())
    return namespace["skill_transparency_matrix"], output.getvalue(), namespace


def test_matrix_runs_immediately_after_agent_definitions_before_every_task(source_notebook):
    ids = [cell["id"] for cell in source_notebook["cells"]]
    start = ids.index("88df3214")
    assert ids[start:start + 4] == ["88df3214", "lab2-skill-transparency-guide",
                                    "lab2-skill-transparency", "lab2-task-configuration"]
    tasks = []
    for index, cell in enumerate(source_notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        for node in ast.walk(ast.parse(_source(cell))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Task":
                tasks.append((index, cell["id"]))
    assert len(tasks) == 3
    assert all(index > ids.index("lab2-skill-transparency") and identifier == "lab2-task-configuration"
               for index, identifier in tasks)
    assert "84aaa3ad" in ids  # The assessed Lab 2 grader retains its original identity.


def test_starter_matrix_reports_actual_permission_excess_and_full_skill_warnings(source_notebook):
    rows, output, _ = _inspect(source_notebook)
    assert [row["role"] for row in rows] == ["Engineering Manager", "Senior Coder", "QA Auditor"]
    manager, coder, qa = rows
    assert manager["actual_tools"] == ["write_code_tool", "approve_code_tool"]
    assert manager["allowed_tools"] == ["approve_code_tool"]
    assert manager["least_privilege"] is False
    assert coder["actual_tools"] == coder["allowed_tools"] == ["write_code_tool"]
    assert qa["actual_tools"] == qa["allowed_tools"] == ["run_tests_tool"]
    assert coder["least_privilege"] is qa["least_privilege"] is True
    for row in rows:
        for skill in row["skill_details"]:
            assert skill["name"] in row["actual_tools"]
            for label in ("Action:", "Input:", "Output:", "Warning:"):
                assert label in skill["description"]
            assert skill["description"] in output
    assert "Actual tools" in output and "Allowed tools" in output and "Least privilege" in output
    assert "runs no commands or real tests" in output


@pytest.mark.parametrize("state,expected_manager", [("permissions_only", True), ("context_only", False), ("fixed", True)])
def test_matrix_reflects_documented_repairs_across_the_split_configuration_cells(source_notebook, repo_root, tmp_path, state, expected_manager):
    path = tmp_path / "02_lab_crewai.ipynb"
    path.write_text(json.dumps(source_notebook))
    repaired = prepared_notebook(path, "lab2", state, solution_root=repo_root)
    rows, _, _ = _inspect(repaired)
    assert rows[0]["least_privilege"] is expected_manager
    assert all(row["least_privilege"] for row in rows[1:])
    tasks = ast.parse(_source(_cell(repaired, "lab2-task-configuration")))
    coder_task = next(node for node in tasks.body if isinstance(node, ast.Assign)
                      and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "coder_task")
    context = next(keyword.value for keyword in coder_task.value.keywords if keyword.arg == "context")
    assert len(context.elts) == (1 if state in {"context_only", "fixed"} else 0)


def test_duplicate_missing_and_extra_capabilities_cannot_receive_a_matching_allowlist(source_notebook):
    _, _, namespace = _inspect(source_notebook)
    build_matrix = namespace["build_skill_transparency"]
    safe = TrapTool("review", "Action: review\nInput: proposal\nOutput: evidence\nWarning: no release.")
    excessive = TrapTool("write", "Action: write\nInput: spec\nOutput: draft\nWarning: no approval.")
    for actual in ([], [safe, safe], [safe, excessive]):
        agent = SimpleNamespace(tools=actual)
        assert not build_matrix({"Manager": agent}, {"Manager": ["review"]})[0]["least_privilege"]
        assert agent.tools is actual
    assert safe.calls == excessive.calls == 0


def test_management_guidance_describes_limits_and_the_complete_rerun_sequence(source_notebook):
    markdown = _source(_cell(source_notebook, "lab2-skill-transparency-guide"))
    assert "Skill Transparency & Least Privilege" in markdown
    assert "Action, Input, Output, and Warning" in markdown
    assert "OS isolation" in markdown
    assert "not model training or fine-tuning" in markdown
    assert "agent definitions, matrix, task configuration, fixture, and audit" in markdown
    assert "does not change tools" in markdown
    assert "[Skill transparency](#lab2-skill-transparency)" in _source(source_notebook["cells"][0])
