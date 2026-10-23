# %% {"id": "aa43b85e", "type": "markdown"}
# # NB0: Course Environment Preflight
#
# Check that your local Python environment can run the course notebooks. This is a diagnostic notebook: it does not start an agent team or call an API.
#
# ## What you interact with
#
# | Action | Your next step | Expected result |
# | --- | --- | --- |
# | **Run** | Run the four code cells from top to bottom with the repository root as the working directory. | Package, execution-mode, directory, and temporary-file checks print their results. |
# | **Edit** | No code edits or TODOs are required. Use [SETUP.md](../SETUP.md) if a required package is missing. | Required packages are available in the selected kernel. Optional package messages do not block the core labs. |
# | **Inspect** | Read the core-package list, repository-marker assertion, and temporary-file confirmation. | All required checks succeed; the temporary probe is deleted. |
# | **Finish** | When the checks pass, open [Lab 1](01_lab_pydantic.ipynb). | You are ready to edit a Pydantic contract. |
#
# The required notebooks use local fixtures after dependency installation. API keys are unnecessary.

# %% {"id": "5eb62b17", "type": "markdown"}
# ## Course path
#
# [Preflight](00_sandbox_preflight.ipynb) → [Lab 1: contracts](01_lab_pydantic.ipynb) → [Lab 2: team configuration](02_lab_crewai.ipynb) → [Lab 3: input and retry controls](03_lab_security.ipynb) → [Capstone](04_capstone.ipynb) → [Software Factory](05_live_software_factory.ipynb) → [Local CI/CD](06_local_cicd.ipynb).
#
# Run the checks below before starting the exercises. The first installation needs package access; the required exercises then use local data and files.

# %% {"id": "preflight-flow", "type": "markdown", "diagram": "resources/diagrams/notebook-preflight-flow.svg"}
# ## Diagnostic flow
#
# ![Preflight exercise flow: run package, execution-mode, repository-directory, and temporary-file checks; fix setup failures before Lab 1.](attachment:notebook-preflight-flow.svg)
#
# Run the checks in order. If a required package or directory check fails, use [SETUP.md](../SETUP.md) and rerun this notebook. When the temporary write check also succeeds, open Lab 1. No learner code edits are required.

# %% {"id": "682ffe7f", "type": "code"}
import importlib.metadata
import importlib.util
import os
import pathlib
import tempfile

CORE_PACKAGES = [
    ("pydantic", "pydantic"),
    ("crewai", "crewai"),
    ("pytest", "pytest"),
    ("jupyterlab", "jupyterlab"),
    ("ipykernel", "ipykernel"),
]
OPTIONAL_PACKAGES = [
    ("fastapi", "fastapi"),
    ("httpx", "httpx"),
    ("langgraph", "langgraph"),
    ("openai", "openai"),
    ("instructor", "instructor"),
    ("python-dotenv", "dotenv"),
]

print("=== Core Package Check ===")
missing_core = []
for package, module in CORE_PACKAGES:
    if importlib.util.find_spec(module) is None:
        missing_core.append(package)
        print(f"MISSING: {package}")
    else:
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = "installed"
        print(f"OK: {package} ({version})")
if missing_core:
    print("Install the core packages using SETUP.md before continuing.")

print("\n=== Optional Extension Check ===")
for package, module in OPTIONAL_PACKAGES:
    status = "available" if importlib.util.find_spec(module) else "not installed (optional)"
    print(f"{package}: {status}")

# %% {"id": "317f03db", "type": "code"}
print("=== Offline Deterministic Mode ===")
USE_LIVE_LLM = False
assert USE_LIVE_LLM is False

live_keys_present = {
    name: bool(os.environ.get(name))
    for name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GROQ_API_KEY"]
}
print("Live keys present but not required:", live_keys_present)
print("Network access required for core notebooks after setup: False")

# %% {"id": "7c2b7c32", "type": "code"}
print("=== Working Directory Check ===")
cwd = pathlib.Path.cwd()
print("cwd:", cwd)

expected_markers = ["notebooks", "ASSIGNMENTS.md", "requirements.txt", "notebook_manifest.yml"]
found = {marker: (cwd / marker).exists() for marker in expected_markers}
print("repo markers:", found)
assert all(found.values()), "Run notebooks from the repository root."

# %% {"id": "552c0d24", "type": "code"}
print("=== /tmp Write Check ===")
tmp_dir = pathlib.Path("/tmp") if pathlib.Path("/tmp").exists() else pathlib.Path(tempfile.gettempdir())
probe = tmp_dir / "managing_multi_agent_teams_preflight.txt"
probe.write_text("sandbox write ok\n")
assert probe.read_text() == "sandbox write ok\n"
probe.unlink()
print(f"OK: wrote and cleaned test file in {tmp_dir}")

# %% {"id": "8e527867", "type": "markdown"}
# ## Read the diagnostic results
#
# - **Core Package Check:** every required package should report `OK`. Optional extension packages may be absent.
# - **Offline Deterministic Mode:** `USE_LIVE_LLM` remains `False`. Reported key presence does not mean the notebook uses those keys.
# - **Working Directory Check:** all repository markers should be `True`. If the assertion fails, restart Jupyter from the repository root as shown in [SETUP.md](../SETUP.md).
# - **Write Check:** the notebook writes, reads, and removes one temporary text file. No course content is modified.
#
# When these checks pass, continue to Lab 1. There is no score or submission for preflight.

# %% {"id": "learner-navigation-00", "type": "markdown"}
# ## Continue or return
#
# After completing this notebook and inspecting its evidence, continue to [Lab 1](01_lab_pydantic.ipynb).
#
# [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index) · [Practical sequence](../README.md#required-practical-sequence)
