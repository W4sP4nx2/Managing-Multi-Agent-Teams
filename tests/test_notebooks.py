from __future__ import annotations

import json
import sys
from types import ModuleType
from pathlib import Path

import pytest


NOTEBOOKS = [
    "00_sandbox_preflight.ipynb",
    "01_hello_multi_agent.ipynb",
    "02_shared_rag_memory.ipynb",
    "03_mcp_tool_gateway.ipynb",
    "04_pydantic_delegation.ipynb",
    "05_self_repair_loop.ipynb",
    "06_dynamic_routing.ipynb",
    "07_debugging_agents.ipynb",
    "08_api_boundaries_async_orchestration.ipynb",
    "09_advanced_fugu_orchestration.ipynb",
    "10_vibe_coding_interface.ipynb",
    "11_enterprise_a2a_perimeter.ipynb",
]


@pytest.mark.notebook
@pytest.mark.parametrize("notebook_name", NOTEBOOKS)
def test_notebook_code_cells_execute(repo_root: Path, notebook_name: str) -> None:
    """Execute generated notebooks offline to catch drift in teaching examples."""

    notebook_path = repo_root / "notebooks" / notebook_name
    notebook = json.loads(notebook_path.read_text())
    module_name = f"notebook_test_{notebook_name.replace('.', '_').replace('-', '_')}"
    module = ModuleType(module_name)
    module.__dict__["__name__"] = module_name
    sys.modules[module_name] = module

    try:
        for index, cell in enumerate(notebook["cells"], start=1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            exec(compile(source, f"{notebook_name}:cell-{index}", "exec"), module.__dict__, module.__dict__)
    finally:
        sys.modules.pop(module_name, None)
