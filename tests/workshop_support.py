"""Execute the actual handouts; apply documented learner repairs only in memory."""
from __future__ import annotations

import ast
import copy
import json
import re
import sys
import textwrap
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from uuid import uuid4


def workshop_paths(root: Path) -> dict[str, Path]:
    import yaml

    manifest = yaml.safe_load((root / "notebook_manifest.yml").read_text())
    sequence = sorted(manifest["required_sequence"], key=lambda entry: entry["order"])
    assert [entry["order"] for entry in sequence] == list(range(7))
    return dict(zip(("preflight", "lab1", "lab2", "lab3", "capstone", "factory", "cicd"),
                    (root / "notebooks" / entry["file"] for entry in sequence), strict=True))


def _solution_nodes(root: Path) -> dict[str, ast.AST]:
    guide = (root / "instructor/solutions/core_notebook_solution_guide.md").read_text()
    nodes = {}
    for block in re.findall(r"```python\s*\n(.*?)```", guide, re.S):
        for node in ast.parse(textwrap.dedent(block)).body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                nodes[node.name] = node
    return nodes


def prepared_notebook(path: Path, kind: str, state: str = "starter", *, solution_root: Path | None = None) -> dict:
    """Repair named AST targets, never cell offsets or the on-disk handout."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if state == "starter" or (kind in {"factory", "cicd"} and state == "fixed"):
        return notebook
    solutions = _solution_nodes(solution_root or path.parent.parent)
    plans = {
        ("lab1", "range_only"): {"research"},
        ("lab1", "extras_only"): {"research"},
        ("lab1", "fixed"): {"research"},
        ("lab2", "permissions_only"): {"manager_tools"},
        ("lab2", "context_only"): {"coder_context"},
        ("lab2", "fixed"): {"manager_tools", "coder_context"},
        ("lab3", "input_only"): {"input"},
        ("lab3", "retries_only"): {"retries"},
        ("lab3", "fixed"): {"input", "retries"},
        ("capstone", "fixed"): {"dev_validator", "coordinator", "security_tools"},
    }
    wanted = plans[kind, state]
    matched = Counter()

    class Repairs(ast.NodeTransformer):
        def visit_ClassDef(self, node):
            if node.name == "StrictResearchOutput" and "research" in wanted:
                replacement = copy.deepcopy(solutions[node.name])
                if state == "range_only":
                    replacement.body = [item for item in replacement.body
                                        if not (isinstance(item, ast.Assign)
                                                and any(isinstance(t, ast.Name) and t.id == "model_config"
                                                        for t in item.targets))]
                if state == "extras_only":
                    for item in replacement.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name) and item.target.id == "confidence_score":
                            item.value = None
                matched["research"] += 1
                return replacement
            if node.name == "SecureToolInput" and "input" in wanted:
                matched["input"] += 1
                return copy.deepcopy(solutions[node.name])
            if node.name == "DevDeliverable" and "dev_validator" in wanted:
                node.body.append(copy.deepcopy(solutions["require_passing_tests"]))
                matched["dev_validator"] += 1
            return self.generic_visit(node)

        def visit_FunctionDef(self, node):
            if node.name == "coordinate_handoff" and "coordinator" in wanted:
                matched["coordinator"] += 1
                return copy.deepcopy(solutions[node.name])
            return self.generic_visit(node)

        def visit_Assign(self, node):
            target = node.targets[0].id if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) else None
            if target == "MAX_RETRIES" and "retries" in wanted:
                node.value = ast.Constant(3)
                matched["retries"] += 1
            if isinstance(node.value, ast.Call):
                edits = {
                    "manager_agent": ("manager_tools", "tools", "approve_code_tool"),
                    "coder_task": ("coder_context", "context", "architect_task"),
                    "security_manager": ("security_tools", "tools", "approve_audit_tool"),
                }
                if target in edits:
                    repair, keyword, value = edits[target]
                    if repair in wanted:
                        for item in node.value.keywords:
                            if item.arg == keyword:
                                item.value = ast.List(elts=[ast.Name(id=value, ctx=ast.Load())], ctx=ast.Load())
                                matched[repair] += 1
            return self.generic_visit(node)

    transformer = Repairs()
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            tree = transformer.visit(ast.parse("".join(cell["source"])))
            cell["source"] = ast.unparse(ast.fix_missing_locations(tree))
    assert dict(matched) == {name: 1 for name in wanted}, f"Repair targets changed: {dict(matched)}; expected {wanted}"
    return notebook


@contextmanager
def notebook_definitions(path: Path, kind: str, names: set[str], state: str = "starter"):
    """Load real pure definitions for unit tests without constructing a Crew."""
    notebook = prepared_notebook(path, kind, state)
    module = ModuleType("workshop_unit_" + uuid4().hex)
    sys.modules[module.__name__] = module
    try:
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            body = []
            for node in ast.parse("".join(cell["source"])).body:
                if isinstance(node, ast.ImportFrom) and node.module in {"pydantic", "typing"}:
                    body.append(node)
                elif isinstance(node, ast.Import) and all(alias.name == "re" for alias in node.names):
                    body.append(node)
                elif isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names:
                    body.append(node)
                elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
                    body.append(node)
            if body:
                exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec", dont_inherit=True), module.__dict__)
        yield module.__dict__
    finally:
        sys.modules.pop(module.__name__, None)
