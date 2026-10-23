"""Run the actual optional pipeline notebook with offline guards and learner edits."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from tests.notebook_runtime import execute_notebook

pytestmark = [pytest.mark.integration, pytest.mark.notebook]

SAFE_DESCRIPTION = "Refactor database schema safely"


def edit_assignment(notebook: dict, cell_id: str, name: str, value) -> None:
    cell = next(cell for cell in notebook["cells"] if cell["id"] == cell_id)
    tree = ast.parse("".join(cell["source"]))
    matches = 0
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == name for target in node.targets):
            node.value = ast.Constant(value)
            matches += 1
    assert matches == 1, f"Learner edit changed: {cell_id}/{name}"
    cell["source"] = ast.unparse(ast.fix_missing_locations(tree))


@pytest.mark.parametrize("description,approval,expected", [
    (None, None, "BLOCKED"),
    (SAFE_DESCRIPTION, None, "SECURITY_APPROVED"),
    (SAFE_DESCRIPTION, False, "BLOCKED"),
    (SAFE_DESCRIPTION, True, "DEPLOYED"),
], ids=["starter", "awaiting-manager", "manager-denied", "repaired-and-approved"])
def test_mock_pipeline_notebook_governance(repo_root, tmp_path, request,
                                         description, approval, expected):
    path = repo_root / "extensions/11_mock_cicd_pipeline.ipynb"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if description is not None:
        edit_assignment(notebook, "mock-cicd-repair", "replacement_description", description)
    if approval is not None:
        edit_assignment(notebook, "mock-cicd-repair-approval", "approve_repaired_feature", approval)
    assertions = f'''
assert {{status.value for status in FeatureStatus}} == {{
    "REQUESTED", "IN_PROGRESS", "QA_PASSED", "SECURITY_APPROVED", "DEPLOYED", "BLOCKED"
}}
assert [item.id for item in feature_batch] == ["FEAT-001", "FEAT-002", "FEAT-003"]
assert feature_batch[0].status == FeatureStatus.DEPLOYED
assert feature_batch[2].status == FeatureStatus.DEPLOYED
assert repaired_feature is feature_batch[1]
assert repaired_feature.status.value == {expected!r}
assert repaired_feature.revision == 2
'''
    if description is not None:
        assertions += f'''
assert repaired_feature.description == {description!r}
assert repaired_feature.qa_passed is True
assert repaired_feature.security_cleared is True
'''
    output_root = request.config.getoption("--notebook-artifacts")
    artifacts = Path(output_root) / f"mock-cicd-{expected.lower()}-{approval}" if output_root else None
    try:
        execute_notebook(notebook, tmp_path, repo_root, assertions, artifacts)
    finally:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before, "Test modified the handout"
