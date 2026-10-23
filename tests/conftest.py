from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def pytest_addoption(parser):
    parser.addoption("--notebook-artifacts", default=None,
                     help="Directory for executed notebook copies and failure diagnostics")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    unclassified = [item.nodeid for item in items
                    if sum(item.get_closest_marker(mark) is not None
                           for mark in ("unit", "integration")) != 1]
    if unclassified:
        raise pytest.UsageError("Every test needs exactly one unit/integration marker:\n"
                                + "\n".join(unclassified))


@pytest.fixture
def repo_root() -> Path:
    return ROOT

