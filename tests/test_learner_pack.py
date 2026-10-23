"""Check the handout independently of files available in the full checkout."""
import json
import re
from io import BytesIO
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
import yaml

from tests.notebook_runtime import execute_notebook
from tests.test_notebooks import management_assertions
from tests.workshop_support import prepared_notebook, workshop_paths
from tools.build_learner_pack import PACKAGE, MARKDOWN_LINK, build, local_target, package_files


@pytest.mark.unit
def test_pack_omits_non_course_files_and_preserves_code_and_deck(repo_root, tmp_path):
    payload = package_files(repo_root)
    assert len([name for name in payload if name.endswith(".ipynb")]) == 8
    assert len([name for name in payload if name.endswith(".pptx")]) == 1
    assert {"slides/managing_multi_agent_teams_6_slides.pptx",
            "slides/managing_multi_agent_teams_6_slides.md",
            "output/pdf/managing_multi_agent_teams_6_slides.pdf"} <= payload.keys()
    assert "slides/managing_multi_agent_teams_workshop_v16.pptx" not in payload
    assert not any("executive_brief" in name for name in payload)
    with ZipFile(BytesIO(payload["slides/managing_multi_agent_teams_6_slides.pptx"])) as deck:
        presentation = ElementTree.fromstring(deck.read("ppt/presentation.xml"))
        assert len(presentation.findall("{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst/*")) == 6
    assert "ASSIGNMENTS.md" in payload
    assert "INSTRUCTOR_PLAYBOOK.md" not in payload
    assert not any(name in payload for name in ("PLAYBOOK.md", "assignments/index.md",
                                                "assignments/assignment_syllabus.md",
                                                "resources/curated_resource_library.md"))
    assert {name for name in payload if name.endswith(".txt")} == {"requirements.txt"}
    assert not any(name.startswith(("instructor/", "tests/", "tools/", "_archive/", ".")) for name in payload)
    assert {"agent_harness.py", "cost_tracker.py", "orchestrator.py", "live_simulation_orchestrator.py",
            "software_factory/workflow.py", "software_factory/simulation_config.json",
            "extensions/live_software_factory.md", "crewai_learning/01_Bridge_Sequential_Crew.ipynb"} <= payload.keys()
    assert not any("live_provider_prototype" in name or name.startswith(".env") for name in payload)
    manifest = yaml.safe_load(payload["notebook_manifest.yml"])
    assert "compatibility_demo" not in manifest and len(manifest["required_sequence"]) == 7
    home = payload["README.md"].decode()
    assert "CrewAI advanced reference" not in home and "Archive" not in home
    assert "live LLM bonus" not in home
    assert "Optional Mock CI/CD Pipeline" not in home
    for name, content in payload.items():
        if name.endswith(".ipynb"):
            before = json.loads((repo_root / name).read_bytes())
            after = json.loads(content)
            assert [c for c in before["cells"] if c["cell_type"] == "code"] == [
                c for c in after["cells"] if c["cell_type"] == "code"]
        elif name.endswith((".pptx", ".txt")):
            assert content == (repo_root / name).read_bytes()
    archive = build(repo_root, tmp_path)
    original = archive.read_bytes()
    assert build(repo_root, tmp_path).read_bytes() == original
    with ZipFile(archive) as zipped:
        assert {name.removeprefix(PACKAGE + "/") for name in zipped.namelist()} == payload.keys()


@pytest.mark.unit
def test_pack_has_no_dangling_local_document_image_or_slide_links(repo_root):
    payload = package_files(repo_root)
    for name, content in payload.items():
        targets = []
        if name.endswith(".md"):
            targets = [m.group(2) for m in MARKDOWN_LINK.finditer(content.decode())]
        elif name.endswith(".ipynb"):
            targets = [m.group(2) for cell in json.loads(content)["cells"]
                       if cell["cell_type"] == "markdown"
                       for m in MARKDOWN_LINK.finditer("".join(cell["source"]))]
        elif name.endswith(".pptx"):
            with ZipFile(BytesIO(content)) as deck:
                targets = [rel.get("Target") for path in deck.namelist()
                           if path.startswith("ppt/slides/_rels/")
                           for rel in ElementTree.fromstring(deck.read(path))
                           if rel.get("TargetMode") == "External"]
        if name.endswith((".md", ".ipynb")):
            texts = ([content.decode()] if name.endswith(".md") else [
                "".join(cell["source"]) for cell in json.loads(content)["cells"]
                if cell["cell_type"] == "markdown"])
            targets.extend(match.group(1) for text in texts
                           for match in re.finditer(r"!\[[^\]\n]*\]\(([^)\s]+)\)", text))
        for target in targets:
            local = local_target(name, target)
            assert local is None or local in payload, (name, target)


@pytest.mark.integration
@pytest.mark.notebook
@pytest.mark.parametrize("kind", ["preflight", "lab1", "lab2", "lab3", "capstone", "factory", "cicd"])
def test_extracted_handouts_run_without_the_repository(repo_root, tmp_path, kind):
    archive = build(repo_root, tmp_path / "delivery")
    with ZipFile(archive) as zipped:
        zipped.extractall(tmp_path / "learner")
    course = tmp_path / "learner" / PACKAGE
    assert not (course / "tests").exists() and not (course / "instructor").exists()
    path = workshop_paths(course)[kind]
    state = "starter" if kind == "preflight" else "fixed"
    # Apply instructor repairs in memory; the extracted pack never contains solutions.
    notebook = prepared_notebook(path, kind, state, solution_root=repo_root)
    assertions = management_assertions(kind, state)
    if kind in {"lab1", "lab2", "lab3"}:
        assertions += f"\nassert {kind}_score == 15\n"
    execute_notebook(notebook, tmp_path / "runtime", course, assertions)
