"""Prove the execution harness fails on accidental external/live calls."""
import nbformat
import pytest
from nbclient.exceptions import CellExecutionError

from tests.notebook_runtime import clean_kernel_environment, execute_notebook


@pytest.mark.unit
def test_kernel_environment_omits_inherited_provider_credentials(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("GROQ_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "synthetic-test-key")
    monkeypatch.setenv("PYTHONPATH", "/synthetic-injected-path")
    env = clean_kernel_environment(tmp_path)
    assert not {"OPENAI_API_KEY", "GROQ_API_KEY", "AWS_ACCESS_KEY_ID", "PYTHONPATH"} & env.keys()
    assert env["OTEL_SDK_DISABLED"] == "true"
    assert env["CREWAI_STORAGE_DIR"].startswith(str(tmp_path))


@pytest.mark.integration
@pytest.mark.notebook
@pytest.mark.parametrize("source", [
    "_GuardedCrew.kickoff(None)",
    "_socket.getaddrinfo('api.invalid', 443)",
    # Swallowing the immediate error must still fail the final no-call assertion.
    "try:\n    _socket.getaddrinfo('api.invalid', 443)\nexcept Exception:\n    pass",
])
def test_runtime_tripwires_fail_closed(repo_root, tmp_path, source):
    notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)])
    with pytest.raises(CellExecutionError, match="OFFLINE_TRIPWIRE|attempted live execution"):
        execute_notebook(notebook, tmp_path, repo_root)
