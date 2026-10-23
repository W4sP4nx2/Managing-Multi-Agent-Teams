"""Run handout copies through a real kernel with no provider credentials."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import nbformat
from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient


OFFLINE_GUARD = r'''
import builtins as _builtins
import ipaddress as _ipaddress
import os as _os
import socket as _socket
import sys as _sys

assert _sys.version_info[:2] == (3, 12), "Workshop verification requires Python 3.12"
assert not any(name.endswith(("_API_KEY", "_ACCESS_TOKEN")) for name in _os.environ)
_offline_attempts = []

def _deny_live_call(*args, **kwargs):
    _offline_attempts.append("live execution or interactive input")
    raise AssertionError("OFFLINE_TRIPWIRE: live execution or interactive input")

def _local_host(host):
    if host == "localhost":
        return True
    try:
        return _ipaddress.ip_address(host).is_loopback
    except (ValueError, TypeError):
        return False

_original_connect = _socket.socket.connect
_original_getaddrinfo = _socket.getaddrinfo

def _offline_connect(sock, address):
    if isinstance(address, tuple) and not _local_host(address[0]):
        _offline_attempts.append("external connection")
        raise AssertionError("OFFLINE_TRIPWIRE: external connection")
    return _original_connect(sock, address)

def _offline_getaddrinfo(host, *args, **kwargs):
    if host is not None and not _local_host(host):
        _offline_attempts.append("external DNS")
        raise AssertionError("OFFLINE_TRIPWIRE: external DNS")
    return _original_getaddrinfo(host, *args, **kwargs)

_socket.socket.connect = _offline_connect
_socket.getaddrinfo = _offline_getaddrinfo
_builtins.input = _deny_live_call

from crewai import Crew as _GuardedCrew
for _method in ("kickoff", "kickoff_async", "kickoff_for_each", "kickoff_for_each_async"):
    if hasattr(_GuardedCrew, _method):
        setattr(_GuardedCrew, _method, _deny_live_call)
'''

OFFLINE_ASSERTIONS = '''
assert _offline_attempts == [], "The required path attempted live execution/network access"
assert globals().get("USE_LIVE_LLM", False) is False
assert not any(name.endswith(("_API_KEY", "_ACCESS_TOKEN")) for name in _os.environ)
'''


def clean_kernel_environment(directory: Path) -> dict[str, str]:
    """Allow system essentials, omit inherited credentials and Python overrides."""
    keep = {
        "PATH", "HOME", "USERPROFILE", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT",
        "TEMP", "TMP", "TMPDIR", "LANG", "LC_ALL", "APPDATA", "LOCALAPPDATA",
    }
    env = {name: value for name, value in os.environ.items() if name.upper() in keep}
    for name in ("IPYTHONDIR", "JUPYTER_CONFIG_DIR", "JUPYTER_DATA_DIR",
                 "JUPYTER_RUNTIME_DIR", "CREWAI_STORAGE_DIR"):
        path = directory / name.lower()
        path.mkdir(parents=True, exist_ok=True)
        env[name] = str(path)
    env.update({
        "PYTHONNOUSERSITE": "1",
        "OTEL_SDK_DISABLED": "true",
        "CREWAI_TELEMETRY_ENABLED": "false",
        "CREWAI_TRACING_ENABLED": "false",
        "DO_NOT_TRACK": "1",
    })
    return env


def execute_notebook(notebook: dict, directory: Path, root: Path,
                     assertions: str = "", artifact_dir: Path | None = None,
                     fixture_crews: bool = False):
    """Own/clean up one kernel; save an executed copy for CI diagnostics."""
    directory.mkdir(parents=True, exist_ok=True)
    kernel_root = directory / "kernels"
    spec = kernel_root / "workshop-verification"
    spec.mkdir(parents=True, exist_ok=True)
    (spec / "kernel.json").write_text(json.dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Workshop verification", "language": "python",
    }), encoding="utf-8")
    specs = KernelSpecManager(kernel_dirs=[str(kernel_root)])

    class VerificationKernelManager(AsyncKernelManager):
        def __init__(self, **kwargs):
            super().__init__(kernel_spec_manager=specs, **kwargs)

    # nbformat.reads normalizes the list-of-lines representation used on disk.
    nb = nbformat.reads(json.dumps(notebook), as_version=4)
    # Only the advanced reference runs real Crew executors with local fixture LLMs.
    # It retains the same external-network, credential, and interaction tripwires.
    guard = OFFLINE_GUARD.split("from crewai import Crew as _GuardedCrew")[0] if fixture_crews else OFFLINE_GUARD
    nb.cells.insert(0, nbformat.v4.new_code_cell(guard, id="test-offline-guard"))
    nb.cells.append(nbformat.v4.new_code_cell(assertions + "\n" + OFFLINE_ASSERTIONS,
                                             id="test-regression-assertions"))
    client = NotebookClient(
        nb, kernel_manager_class=VerificationKernelManager,
        kernel_name="workshop-verification", timeout=40, startup_timeout=60,
        allow_errors=False, store_widget_state=False,
        resources={"metadata": {"path": str(root)}},
    )
    try:
        return client.execute(env=clean_kernel_environment(directory))
    finally:
        target = artifact_dir or directory
        target.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, target / "executed.ipynb")
