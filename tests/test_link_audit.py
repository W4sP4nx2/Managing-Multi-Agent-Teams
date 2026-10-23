"""Safe, byte-preserving link maintenance; HTTP observations are always mocked."""
from collections import Counter
from copy import deepcopy
import json
import subprocess
from zipfile import ZipFile

import pytest

from tools import audit_links as links
from tools.build_core_notebooks import notebook_from_source

pytestmark = pytest.mark.unit


def test_captcha_script_does_not_make_a_successful_document_uncertain(tmp_path):
    body = b'<title>Repository documentation</title><script>const captcha = "cf-chl-library";</script><h1>Guide</h1>'
    report = audit_text(tmp_path, "[guide](https://example.test/guide)\n", external=True,
                        fetcher=lambda url: links.FetchResult(200, url, body, "text/html"))
    assert report["findings"][0]["status"] == "verified_external"
    assert report["edits"] == []


def write(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def findings(report):
    return {finding["target"]: finding for finding in report["findings"]}


def audit_text(root, text, **kwargs):
    write(root, "README.md", text)
    return links.audit(root, ["README.md"], **kwargs)


def test_valid_content_keeps_its_exact_bytes_and_check_writes_nothing(tmp_path):
    write(tmp_path, "guide (final).md", "# Heading\n<a id='explicit'></a>\n")
    text = ("# Home\n[title](<guide (final).md#Heading> 'a title')\n"
            "![image](image%20one.svg)\n[section](#home)\n"
            "<a href='guide%20%28final%29.md#explicit'>HTML</a>\n"
            "[external](https://example.test/?a=1&b=2)\n")
    # Use a compliant case-sensitive heading spelling: compliant content is never normalized.
    text = text.replace("#Heading", "#heading")
    write(tmp_path, "image one.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
    path = write(tmp_path, "README.md", text)
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    report = links.audit(tmp_path, ["README.md"])
    assert report["summary"]["repairs"] == 0
    assert report["edits"] == []
    assert links.apply_report(tmp_path, report) == []
    assert path.read_bytes() == text.encode()
    assert before == {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert findings(report)["https://example.test/?a=1&b=2"]["status"] == "unverified_external"


def test_relative_resolution_wins_over_root_and_unique_basename(tmp_path):
    write(tmp_path, "guide.md", "# Root\n")
    write(tmp_path, "docs/guide.md", "# Local\n")
    write(tmp_path, "other/guide.md", "# Other\n")
    write(tmp_path, "docs/source.md", "[local](guide.md#local)\n")
    report = links.audit(tmp_path, ["docs/source.md"])
    assert report["summary"]["repairs"] == 0
    assert findings(report)["guide.md#local"]["resolved_path"] == "docs/guide.md"


def test_root_alignment_and_unique_disk_mapping_are_repaired(tmp_path):
    write(tmp_path, "guide.md", "# Guide\n")
    write(tmp_path, "moved/unique.md", "# Unique\n")
    write(tmp_path, "docs/source.md", "See [root](guide.md) and [moved](old/unique.md).\n")
    report = links.audit(tmp_path, ["docs/source.md"])
    assert [f["status"] for f in report["findings"]] == ["repair_local", "repair_local"]
    assert links.apply_report(tmp_path, report) == ["docs/source.md"]
    assert (tmp_path / "docs/source.md").read_text() == "See [root](../guide.md) and [moved](../moved/unique.md).\n"


def test_consolidation_mapping_repairs_path_and_fragment(tmp_path):
    write(tmp_path, "hub.md", '# New heading\n<a id="overview"></a>\n')
    write(tmp_path, links.REDIRECTS, json.dumps([{
        "source": "old.md", "target": "hub.md", "anchor": "overview",
        "fragments": {"old-heading": "new-heading"},
    }]))
    report = audit_text(tmp_path, "See [mapped](old.md#old-heading) and [page](old.md).\n")
    rows = findings(report)
    assert rows["old.md#old-heading"]["replacement"] == "hub.md#new-heading"
    assert rows["old.md"]["replacement"] == "hub.md#overview"
    links.apply_report(tmp_path, report)
    assert links.audit(tmp_path, ["README.md"])["edits"] == []


def test_ambiguous_local_reference_is_preserved_with_candidates(tmp_path):
    write(tmp_path, "one/topic.md", "one")
    write(tmp_path, "two/topic.md", "two")
    report = audit_text(tmp_path, "See [topic](gone/topic.md).\n")
    finding = report["findings"][0]
    assert finding["status"] == "ambiguous_local"
    assert finding["candidates"] == ["one/topic.md", "two/topic.md"]
    assert report["edits"] == []


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.mark.parametrize("historical", [False, True])
def test_missing_worktree_path_verified_in_index_or_history_is_preserved(tmp_path, historical):
    git(tmp_path, "init", "-q")
    write(tmp_path, "deleted.md", "# Archived in Git\n")
    git(tmp_path, "add", "deleted.md")
    if historical:
        git(tmp_path, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.test",
            "commit", "-qm", "Fixture")
        git(tmp_path, "rm", "-q", "deleted.md")
    else:
        (tmp_path / "deleted.md").unlink()
    report = audit_text(tmp_path, "[recoverable](deleted.md)\n")
    finding = report["findings"][0]
    assert finding["status"] == "git_only"
    assert finding["git_object"].endswith(":deleted.md")
    assert report["edits"] == []


def test_missing_local_wrappers_are_removed_without_changing_surrounding_text(tmp_path):
    report = audit_text(tmp_path, "Before [**label**](missing.md) after.\n"
                        "- [only invalid reference](missing-two.md)\n"
                        "Keep this sentence.\n")
    assert links.apply_report(tmp_path, report) == ["README.md"]
    assert (tmp_path / "README.md").read_text() == "Before **label** after.\nKeep this sentence.\n"
    again = links.audit(tmp_path, ["README.md"])
    assert again["edits"] == []
    assert links.apply_report(tmp_path, again) == []


def test_reference_style_removal_handles_shared_definition_without_overlaps(tmp_path):
    report = audit_text(tmp_path, "See [first][topic] and [second][topic].\n\n[topic]: missing.md\n")
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text() == "See first and second.\n\n"


def test_reference_definition_repair_updates_every_use_once(tmp_path):
    write(tmp_path, "actual/target.md", "# Actual\n")
    report = audit_text(tmp_path, "See [first][topic] and [second][topic].\n\n[topic]: target.md\n")
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text().endswith("[topic]: actual/target.md\n")
    assert links.audit(tmp_path, ["README.md"])["edits"] == []


def test_fenced_inline_escaped_and_html_code_examples_are_ignored(tmp_path):
    text = ("```md\n[example](missing.md)\n<img src='missing.png'>\n```\n"
            "    [indented](also-missing.md)\n\n"
            "`[inline](missing.md)` and `<a href='missing.md'>x</a>`.\n"
            "\\[escaped](missing.md)\n"
            "<pre><a href='missing.md'>example</a></pre>\n")
    report = audit_text(tmp_path, text)
    assert report["findings"] == []
    assert report["edits"] == []


def test_mixed_inline_html_does_not_turn_code_example_into_a_real_link(tmp_path):
    text = "<span>Note</span>: `<a href='missing.md'>sample</a>`.\n"
    report = audit_text(tmp_path, text)
    assert report["findings"] == []
    assert report["edits"] == []


def test_generated_duplicate_headings_and_explicit_html_ids(tmp_path):
    text = "# Repeat\n# Repeat\n# Repeat-1\n# Repeat\n<a id='stable'></a><a name='legacy'></a>\n"
    assert links.document_anchors(text) == {"repeat", "repeat-1", "repeat-1-1", "repeat-2", "stable", "legacy"}
    write(tmp_path, "target.md", text)
    report = audit_text(tmp_path, " ".join(f"[a](target.md#{anchor})" for anchor in links.document_anchors(text)))
    assert report["summary"]["repairs"] == 0


def test_explicit_anchor_examples_inside_markdown_code_do_not_count_as_targets():
    text = ("```html\n<a id='fenced-example'></a>\n```\n"
            "`<a id='inline-example'></a>`\n<a id='real'></a>\n")
    assert links.document_anchors(text) == {"real"}


def test_unambiguous_heading_spelling_is_repaired(tmp_path):
    write(tmp_path, "target.md", "# A real heading\n")
    report = audit_text(tmp_path, "See [heading](target.md#A%20real%20heading).\n")
    assert report["findings"][0]["replacement"] == "target.md#a-real-heading"


def notebook(markdown_cells):
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": [
        {"id": f"cell-{index}", "cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}
        for index, text in enumerate(markdown_cells)] + [
        {"id": "code", "cell_type": "code", "metadata": {}, "source": ["# TODO: preserve\n", "x = 1\n"],
         "outputs": [], "execution_count": None}]}


def test_notebook_anchors_span_cells_and_include_cell_ids(tmp_path):
    write(tmp_path, "notebooks/target.ipynb", json.dumps(notebook(["# Repeat\n", "# Repeat\n"])))
    report = audit_text(tmp_path, "[one](notebooks/target.ipynb#repeat) [two](notebooks/target.ipynb#repeat-1) "
                        "[cell](notebooks/target.ipynb#cell-1)\n")
    assert report["summary"]["repairs"] == 0


def test_notebook_json_repairs_preserve_code_ids_and_metadata(tmp_path):
    before = notebook(["Before [missing](gone.md) after.\n"])
    before["metadata"] = {"custom": "keep"}
    path = write(tmp_path, "notebooks/target.ipynb", json.dumps(before, indent=1) + "\n")
    report = links.audit(tmp_path, ["notebooks/target.ipynb"])
    links.apply_report(tmp_path, report)
    after = json.loads(path.read_text())
    expected = deepcopy(before)
    expected["cells"][0]["source"] = ["Before missing after.\n"]
    assert after == expected


def test_canonical_notebook_source_is_repaired_before_regeneration(tmp_path):
    source = write(tmp_path, "tools/notebook_sources/lesson.py",
                   '# %% {"id": "intro", "type": "markdown"}\n'
                   '# See [missing](gone.md) here.\n\n'
                   '# %% {"id": "exercise", "type": "code"}\n# TODO: preserve\nx = 1\n')
    before = notebook_from_source(source)
    path = write(tmp_path, "notebooks/lesson.ipynb", json.dumps(before, indent=2) + "\n")
    report = links.audit(tmp_path, ["notebooks/lesson.ipynb"])
    assert {e["path"] for e in report["edits"]} == {"tools/notebook_sources/lesson.py"}
    assert set(links.apply_report(tmp_path, report)) == {"notebooks/lesson.ipynb", "tools/notebook_sources/lesson.py"}
    after = json.loads(path.read_text())
    assert after == notebook_from_source(source)
    assert after["cells"][1] == before["cells"][1]
    assert after["cells"][0]["id"] == "intro"
    assert "See missing here." in source.read_text()


def test_stale_source_or_anchor_target_prevents_all_repairs(tmp_path):
    write(tmp_path, "target.md", "# Heading\n")
    report = audit_text(tmp_path, "See [anchor](target.md#missing) and [dead](gone.md).\n")
    original = (tmp_path / "README.md").read_bytes()
    write(tmp_path, "target.md", "# Heading\n# Missing\n")
    with pytest.raises(ValueError, match="Stale"):
        links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_bytes() == original


def test_new_untracked_target_invalidates_recorded_removal(tmp_path):
    git(tmp_path, "init", "-q")
    report = audit_text(tmp_path, "See [new](new.md).\n")
    write(tmp_path, "new.md", "# This target now exists\n")
    with pytest.raises(ValueError, match="(?i)(stale|changed|resolution)"):
        links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text() == "See [new](new.md).\n"


def test_changed_git_index_prevents_apply(tmp_path):
    git(tmp_path, "init", "-q")
    report = audit_text(tmp_path, "See [missing](gone.md).\n")
    write(tmp_path, "new.txt", "new")
    git(tmp_path, "add", "new.txt")
    with pytest.raises(ValueError, match="Git index changed"):
        links.apply_report(tmp_path, report)


def test_archive_can_be_linked_but_never_loaded_or_modified(tmp_path):
    archived = write(tmp_path, "_archive/old.md", "# Old\n[bad](missing.md)\n")
    before = archived.read_bytes()
    report = audit_text(tmp_path, "[archive](_archive/old.md#old)\n")
    assert report["summary"]["repairs"] == 0
    assert links.apply_report(tmp_path, report) == []
    assert archived.read_bytes() == before
    with pytest.raises(ValueError, match="Refusing editable"):
        links.audit(tmp_path, ["_archive/old.md"])
    forged = deepcopy(report)
    forged["inputs"]["_archive/old.md"] = links.digest(before)
    forged["edits"] = [{"path": "_archive/old.md", "start": 0, "end": 1, "old": "#", "new": ""}]
    with pytest.raises(ValueError, match="Refusing repair"):
        links.apply_report(tmp_path, forged)
    assert archived.read_bytes() == before


def test_source_symlink_outside_root_is_never_loaded(tmp_path):
    outside = tmp_path.parent / (tmp_path.name + "-outside.md")
    outside.write_text("[missing](gone.md)\n")
    try:
        (tmp_path / "escape.md").symlink_to(outside)
        with pytest.raises(ValueError, match="Refusing editable"):
            links.audit(tmp_path, ["escape.md"])
    finally:
        outside.unlink()


def test_archive_alias_cannot_be_used_to_mutate_frozen_content(tmp_path):
    archived = write(tmp_path, "_archive/old.md", "[missing](gone.md)\n")
    (tmp_path / "alias.md").symlink_to(archived)
    with pytest.raises(ValueError, match="Refusing editable"):
        links.audit(tmp_path, ["alias.md"])
    assert archived.read_text() == "[missing](gone.md)\n"


@pytest.mark.parametrize("statuses, expected, call_count", [
    ([404, 404], "dead_external", 2),
    ([410, 410], "dead_external", 2),
    ([404, 200], "verified_external", 2),
    ([404, 503], "uncertain_external", 2),
    ([401], "uncertain_external", 1),
    ([403], "uncertain_external", 1),
    ([429], "uncertain_external", 1),
    ([500], "uncertain_external", 1),
    ([None], "uncertain_external", 1),
])
def test_http_failures_need_bounded_confirmation_before_removal(tmp_path, statuses, expected, call_count):
    responses = iter(statuses)
    calls = []

    def fetch(url):
        calls.append(url)
        return links.FetchResult(next(responses), url, error="fixture")

    report = audit_text(tmp_path, "[site](https://example.test/page)\n", external=True, fetcher=fetch)
    assert report["findings"][0]["status"] == expected
    assert len(calls) == call_count
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text() == ("site\n" if expected == "dead_external" else "[site](https://example.test/page)\n")


def test_working_redirect_keeps_original_url_spelling(tmp_path):
    report = audit_text(tmp_path, "[site](https://example.test/old)\n", external=True,
                        fetcher=lambda url: links.FetchResult(200, "https://example.test/new"))
    assert report["findings"][0]["status"] == "verified_external"
    assert report["findings"][0]["final_url"] == "https://example.test/new"
    assert report["edits"] == []


@pytest.mark.parametrize("fragment, truncated, expected", [
    ("real", False, "verified_external"),
    ("missing", False, "unverified_external_anchor"),
    ("real", True, "unverified_external_anchor"),
])
def test_external_anchors_are_only_verified_with_complete_matching_html(tmp_path, fragment, truncated, expected):
    report = audit_text(tmp_path, f"[site](https://example.test/page#{fragment})\n", external=True,
                        fetcher=lambda url: links.FetchResult(200, url, b'<h1 id="real">A</h1>', "text/html", truncated=truncated))
    assert report["findings"][0]["status"] == expected
    assert report["edits"] == []


def test_confirmed_dead_url_uses_only_verified_configured_replacement(tmp_path):
    calls = Counter()

    def fetch(url):
        calls[url] += 1
        return links.FetchResult(404 if url.endswith("/old") else 200, url)

    report = audit_text(tmp_path, "[site](https://example.test/old)\n", external=True, fetcher=fetch,
                        replacements={"https://example.test/old": "https://example.test/new"})
    assert report["findings"][0]["status"] == "repair_external"
    assert calls == {"https://example.test/old": 2, "https://example.test/new": 1}
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text() == "[site](https://example.test/new)\n"


def test_replacement_with_unverified_anchor_is_not_installed(tmp_path):
    def fetch(url):
        return links.FetchResult(404 if url.endswith("/old") else 200, url, b'<h1 id="real">A</h1>', "text/html")

    report = audit_text(tmp_path, "[site](https://example.test/old)\n", external=True, fetcher=fetch,
                        replacements={"https://example.test/old": "https://example.test/new#missing"})
    assert not any(edit["new"] == "https://example.test/new#missing" for edit in report["edits"])


def test_markdown_autolinks_are_audited_and_dead_urls_become_plain_text(tmp_path):
    report = audit_text(tmp_path, "Visit <https://example.test/dead>.\n", external=True,
                        fetcher=lambda url: links.FetchResult(404, url))
    assert report["summary"]["references"] == 1
    assert report["findings"][0]["status"] == "dead_external"
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text() == "Visit https://example.test/dead.\n"


def test_antibot_error_page_is_not_evidence_to_remove_a_working_url(tmp_path):
    challenge = b"<title>Just a moment...</title>Cloudflare: Enable JavaScript and cookies to continue"
    report = audit_text(tmp_path, "[site](https://example.test/protected)\n", external=True,
                        fetcher=lambda url: links.FetchResult(404, url, challenge, "text/html"))
    assert report["findings"][0]["status"] == "uncertain_external"
    assert report["edits"] == []


def test_static_repository_root_path_literals_are_checked_and_preserved(tmp_path):
    write(tmp_path, "docs/guide.md", "# Guide\n")
    write(tmp_path, "nested/source.md", "Read `docs/guide.md` before class.\n")
    report = links.audit(tmp_path, ["nested/source.md"])
    assert findings(report)["docs/guide.md"]["status"] == "valid_local"
    assert report["edits"] == []
    assert links.apply_report(tmp_path, report) == []
    assert (tmp_path / "nested/source.md").read_text() == "Read `docs/guide.md` before class.\n"


def test_static_paths_skip_examples_generated_outputs_globs_and_environments(tmp_path):
    text = ("Illustrative example: `example/path.md`.\n"
            "Runtime output: `output/results.json`.\n"
            "Dependencies: `.venv/bin/python` and `node_modules/package/index.js`.\n"
            "Pattern: `notebooks/*.ipynb`.\n"
            "```sh\ncat docs/nonexistent.md\n```\n")
    report = audit_text(tmp_path, text)
    assert report["findings"] == []
    assert report["edits"] == []


def test_inline_shell_commands_keep_interpreter_arguments_and_working_directory(tmp_path):
    write(tmp_path, "tools/check_readiness.py", "print('ready')\n")
    write(tmp_path, "requirements/maintenance.txt", "pytest==8.4.2\n")
    write(tmp_path, "extensions/setup.sh", "#!/bin/sh\n")
    text = ("Run `python tools/check_readiness.py`.\n"
            "Install with `python -m pip install -r requirements/maintenance.txt`.\n"
            "Then run `bash extensions/setup.sh`.\n")
    write(tmp_path, "docs/source.md", text)
    report = links.audit(tmp_path, ["docs/source.md"])
    assert report["edits"] == []
    assert links.apply_report(tmp_path, report) == []
    assert (tmp_path / "docs/source.md").read_text() == text


def test_missing_literal_path_does_not_destroy_useful_sentence(tmp_path):
    report = audit_text(tmp_path, "This paragraph describes `missing.md` for future reference.\n")
    assert "missing.md" in findings(report)
    links.apply_report(tmp_path, report)
    assert (tmp_path / "README.md").read_text().startswith("This paragraph describes ")
    assert "for future reference." in (tmp_path / "README.md").read_text()


def test_clean_cli_check_is_offline_and_writes_no_report_without_request(tmp_path, capsys):
    write(tmp_path, "README.md", "# Home\n[web](https://example.test/)\n")
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert links.main(["--root", str(tmp_path), "check"]) == 0
    assert "External URL availability was not checked" in capsys.readouterr().out
    assert before == {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}


def test_cli_saves_readable_evidence_and_applies_the_saved_report(tmp_path):
    write(tmp_path, "README.md", "See [missing](gone.md) here.\n")
    report_path = tmp_path / "output/audit.json"
    assert links.main(["--root", str(tmp_path), "check", "--report", str(report_path)]) == 1
    report = json.loads(report_path.read_text())
    assert report["inputs"]["README.md"]
    assert report["findings"][0]["line"] == 1
    readable = report_path.with_suffix(".md").read_text()
    assert "missing_local" in readable and "gone.md" in readable
    assert (tmp_path / "README.md").read_text() == "See [missing](gone.md) here.\n"
    assert links.main(["--root", str(tmp_path), "apply", "--from-report", str(report_path)]) == 0
    assert (tmp_path / "README.md").read_text() == "See missing here.\n"


def test_invalid_repair_span_is_rejected_before_any_file_is_written(tmp_path):
    write(tmp_path, "second.md", "See [also missing](gone.md).\n")
    write(tmp_path, "README.md", "See [missing](gone.md).\n")
    report = links.audit(tmp_path, ["README.md", "second.md"])
    before = {name: (tmp_path / name).read_bytes() for name in ["README.md", "second.md"]}
    report["edits"][-1]["old"] = "not the audited bytes"
    with pytest.raises(ValueError, match="Repair span"):
        links.apply_report(tmp_path, report)
    assert before == {name: (tmp_path / name).read_bytes() for name in before}


def test_pptx_removes_dead_relationship_and_click_but_keeps_other_members(tmp_path):
    path = tmp_path / "deck.pptx"
    rel = ('<Relationships><Relationship Id="rId1" TargetMode="External" '
           'Target="https://example.test/dead" Type="hyperlink"/></Relationships>')
    slide = '<p:sld><a:r><a:rPr><a:hlinkClick r:id="rId1"/></a:rPr><a:t>label</a:t></a:r></p:sld>'
    with ZipFile(path, "w") as archive:
        archive.writestr("ppt/slides/_rels/slide1.xml.rels", rel)
        archive.writestr("ppt/slides/slide1.xml", slide)
        archive.writestr("keep.bin", b"untouched")
    report = links.audit(tmp_path, ["deck.pptx"], external=True,
                         fetcher=lambda url: links.FetchResult(410, url))
    links.apply_report(tmp_path, report)
    with ZipFile(path) as archive:
        assert b"Relationship Id" not in archive.read("ppt/slides/_rels/slide1.xml.rels")
        assert b"hlinkClick" not in archive.read("ppt/slides/slide1.xml")
        assert b"label" in archive.read("ppt/slides/slide1.xml")
        assert archive.read("keep.bin") == b"untouched"


def test_active_curriculum_has_no_pending_local_link_repairs(repo_root):
    # Collected by the unit stage of tools/check_readiness.py; deliberately offline.
    report = links.audit(repo_root)
    pending = [finding for finding in report["findings"] if finding["action"] != "keep"]
    assert pending == [], json.dumps(pending, indent=2)
    assert not any(name.startswith("_archive/") for name in report["sources"])
