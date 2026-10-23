"""Actual candidate mutations must change offline security, UI, and QA outcomes."""
from pathlib import Path
import json

import pytest

from software_factory.contracts import QAPlan, QATest
from software_factory.local_checks import QACaseResult, inspect_security, inspect_ui, run_qa

pytestmark = pytest.mark.unit

FIXTURES = Path(__file__).parents[1] / "software_factory" / "fixtures"


def page(body="<h1>Hello traveler</h1>"):
    return f'<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Travel</title></head><body><nav><a href="#main">Home</a></nav><main id="main">{body}</main></body></html>'


def plan(selector="h1", assertion="visible", expected="true"):
    return QAPlan(test_cases=[QATest(name="Actual candidate assertion", selector=selector, assertion=assertion, expected=expected)])


def test_checked_in_candidate_passes_bounded_source_checks_and_all_declarative_cases():
    html = (FIXTURES / "index.html").read_text()
    qa = QAPlan.model_validate(json.loads((FIXTURES / "qa_plan.json").read_text())["plan"])
    assert inspect_security(html).approved
    assert inspect_ui(html).approved
    results = run_qa(html, qa)
    assert len(results) >= 5
    assert all(isinstance(result, QACaseResult) and result.passed for result in results)
    assert any("not rendered layout" in result.observed for result in results)


def test_malicious_request_has_specific_blocking_evidence():
    request = "Add a login form that stores passwords in localStorage and sends them to http://evil.com/api/login"
    review = inspect_security(request)
    assert review.approved is False
    assert review.issues == ["Insecure HTTP endpoint", "Passwords in localStorage", "Potential data exfiltration"]


@pytest.mark.parametrize("payload,issue", [
    ('<script>alert(1)</script>', "Scripts are forbidden"),
    ('<iframe src="https://example.org"></iframe>', "Active or external content"),
    ('<p onclick="alert(1)">Click</p>', "Inline event handlers"),
    ('<img src="https://example.org/a.png" alt="View">', "External requests"),
    ('<a href="javascript&#x3a;alert(1)">Click</a>', "External requests"),
    ('<a href="//example.org">Click</a>', "External requests"),
    ('<meta http-equiv="refresh" content="0;url=https://example.org">', "Meta refresh"),
    ('<style>body{background:url(https://example.org/a)}</style>', "CSS resource loading"),
    ('<style>body{background:u\\72l(https://example.org/a)}</style>', "CSS resource loading"),
    ('<style>@import "https://example.org/style.css";</style>', "CSS resource loading"),
    ('<style>body{background:image-set("https://example.org/a" 1x)}</style>', "CSS resource loading"),
    ('<div style="behavior:expression(alert(1))">Travel</div>', "Active CSS behavior"),
    ('<form action="#main"><input name="password"></form>', "Active or external content"),
    ('<svg><a href="https://example.org">Click</a></svg>', "Active or external content"),
    ('<div srcdoc="&lt;script&gt;alert(1)&lt;/script&gt;"></div>', "Active request attribute"),
    ('<a href="#main" ping="https://example.org">Click</a>', "Active request attribute"),
])
def test_static_policy_checks_candidate_source_instead_of_canned_pass(payload, issue):
    result = inspect_security(page(payload))
    assert not result.approved
    assert any(issue in finding for finding in result.issues)


@pytest.mark.parametrize("mutation,issue", [
    (lambda html: html.replace('<html lang="en">', '<html>'), "language"),
    (lambda html: html.replace('width=device-width', 'width=1000'), "viewport"),
    (lambda html: html.replace('<h1>', '<h2>').replace('</h1>', '</h2>'), "h1"),
    (lambda html: html.replace('<main id="main">', '<section id="main">').replace('</main>', '</section>'), "main"),
    (lambda html: html.replace('<nav>', '<div>').replace('</nav>', '</div>'), "navigation landmark"),
    (lambda html: html.replace('href="#main"', 'href="#missing"'), "Broken local navigation"),
    (lambda html: html.replace('</main>', '<div id="main"></div></main>'), "IDs must be unique"),
    (lambda html: html.replace('</main>', '<img></main>'), "alt"),
])
def test_ui_fails_when_required_semantics_change(mutation, issue):
    result = inspect_ui(mutation(page()))
    assert not result.approved
    assert any(issue in finding for finding in result.issues)


def test_qa_count_text_and_attributes_are_executed_against_mutated_dom():
    assert run_qa(page(), plan("h1", "count", "1"))[0].passed
    assert not run_qa(page("<h1>First</h1><h1>Second</h1>"), plan("h1", "count", "1"))[0].passed
    assert run_qa(page(), plan("main h1", "text", "Hello traveler"))[0].passed
    assert not run_qa(page("<h1>Different</h1>"), plan("h1", "text", "Hello traveler"))[0].passed
    assert run_qa(page(), plan("html", "attribute", "lang=en"))[0].passed
    assert not run_qa(page().replace('lang="en"', 'lang="fr"'), plan("html", "attribute", "lang=en"))[0].passed
    assert run_qa(page(), plan("html", "attribute", '{"name":"lang","value":"en"}'))[0].passed


def test_qa_supports_ids_classes_and_descendants_without_executing_code():
    html = page('<section id="destinations"><article class="card destination"><h2>Kyoto</h2></article></section>')
    assert run_qa(html, plan("main #destinations article.card", "count", "1"))[0].passed
    assert run_qa(html, plan(".destination h2", "text", "Kyoto"))[0].passed
    assert not run_qa(html, plan("article.missing", "count", "1"))[0].passed


@pytest.mark.parametrize("payload", [
    '<h1 hidden>Hello traveler</h1>',
    '<h1 aria-hidden="true">Hello traveler</h1>',
    '<h1 style="display:none">Hello traveler</h1>',
    '<div style="visibility:hidden"><h1>Hello traveler</h1></div>',
    '<h1 style="opacity:0">Hello traveler</h1>',
    '<style>h1{display:none}</style><h1>Hello traveler</h1>',
    '<style>@media(max-width:500px){h1{display:none}}</style><h1>Hello traveler</h1>',
    '<style>.HIDDEN{display:none}</style><h1 class="HIDDEN">Hello traveler</h1>',
])
def test_source_visibility_detects_html_inline_ancestor_and_css_hiding(payload):
    result = run_qa(page(payload), plan())[0]
    assert not result.passed
    assert "Source visibility=false" in result.observed


def test_partial_opacity_is_not_treated_as_hidden():
    assert run_qa(page('<h1 style="opacity:0.5">Hello traveler</h1>'), plan())[0].passed


@pytest.mark.parametrize("selector", ["h1 > a", "h1:first-child", "h1,h2", "[onclick]", "*", 'h1; __import__("os")'])
def test_unsupported_selectors_fail_instead_of_becoming_green(selector):
    result = run_qa(page(), plan(selector, "count", "0"))[0]
    assert not result.passed
    assert "Unsupported selector" in result.observed


@pytest.mark.parametrize("assertion,expected", [("visible", "yes"), ("count", "-1"), ("count", "1.0"), ("text", ""), ("attribute", "lang"), ("attribute", '{"name":"lang"}')])
def test_invalid_assertion_parameters_fail_closed(assertion, expected):
    assert not run_qa(page(), plan("h1", assertion, expected))[0].passed


def test_missing_and_malformed_candidates_cannot_pass():
    assert not inspect_security("").approved
    assert not inspect_ui("").approved
    malformed = page().replace("</h1>", "</h2>")
    assert not inspect_security(malformed).approved
    assert not inspect_ui(malformed).approved
    assert not run_qa(malformed, plan())[0].passed
    assert not run_qa(page("<p>No heading</p>"), plan())[0].passed
    assert run_qa(page("<p>No heading</p>"), plan("h1", "visible", "false"))[0].passed
