"""Instructor runner for Exercise 2.1.

The implementation lives in ex2_memory_system_starter.py because the live
coding exercise asks learners to open that file directly.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_solution_module():
    module_path = Path(__file__).with_name("ex2_memory_system_starter.py")
    spec = importlib.util.spec_from_file_location("ex2_type_safe_solution", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    solution = load_solution_module()
    report = solution.run_customer_service_crew()
    assert report.recommended_action == "refund_review"
    solution.demo_invalid_output_rejected()
