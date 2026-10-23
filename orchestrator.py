"""Course demo entry point. No API credentials, network calls, or paid mode."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from agent_harness import AgentHarness
from software_factory.workflow import ApprovalRequest, DEFAULT_REQUEST, FactoryOrchestrator, MALICIOUS_REQUEST


def terminal_approval(request: ApprovalRequest) -> bool:
    print(f"\nHUMAN APPROVAL REQUIRED · {request.stage}")
    print(request.action)
    print(f"Simulated stage cost: ${request.simulated_cost} | Actual cost: $0.00")
    print(f"Subject SHA-256: {request.subject_sha256}")
    print(json.dumps(request.evidence, indent=2))
    try:
        return input("Approve this stage? Type yes or no: ").strip().casefold() == "yes"
    except (EOFError, KeyboardInterrupt):
        print("\nNo approval received; the next action is blocked.")
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic travel-site software factory; actual API cost $0.00")
    parser.add_argument("--mode", choices=("simulation", "replay"), default="simulation")
    parser.add_argument("--workspace", type=Path, default=Path("output/software-factory"))
    parser.add_argument("--output", type=Path, default=Path("index.html"))
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument("--config", type=Path, help="Reviewed offline role labels and simulated costs JSON")
    parser.add_argument("--simulated-budget", default=None, help="Override the profile's simulated run budget")
    parser.add_argument("--delay-seconds", type=float, default=1.5, help="Simulated work delay per role; no actual model thinking")
    parser.add_argument("--no-input", action="store_true", help="Deny pending human decisions; never auto-approve")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--security-demo", action="store_true")
    args = parser.parse_args(argv)
    harness = AgentHarness(mode=args.mode, config=args.config)
    if args.security_demo:
        review = harness.get_security_review(MALICIOUS_REQUEST)
        print(f"Blocked: {not review['approved']}")
        print(f"Issues: {review['issues']}")
        print("Local deny rules demonstrated; actual API cost $0.00; no files published.")
        return 0 if not review["approved"] and len(review["issues"]) == 3 else 1
    if args.check_only:
        from software_factory.local_checks import inspect_security, inspect_ui, run_qa
        plan = harness.plan(DEFAULT_REQUEST)
        artifact = harness.build_site(DEFAULT_REQUEST, plan)
        cases = run_qa(artifact.html, harness.generate_qa(artifact))
        checks = {"git_available": shutil.which("git") is not None,
                  "security_source_checks": inspect_security(artifact.html).approved,
                  "ui_source_checks": inspect_ui(artifact.html).approved,
                  "qa_cases_passed": bool(cases) and all(case.passed for case in cases),
                  "api_keys_required": False, "provider_calls": 0, "actual_cost": "0.00"}
        print(json.dumps(checks, indent=2))
        return 0 if all(checks[key] for key in ("git_available", "security_source_checks", "ui_source_checks", "qa_cases_passed")) else 1
    runner = FactoryOrchestrator(args.workspace, harness=harness, publish_path=args.output,
                                 simulated_budget=args.simulated_budget, delay_seconds=args.delay_seconds,
                                 approval=(lambda request: False) if args.no_input else terminal_approval)
    result = runner.run(args.request)
    print(result.model_dump_json(indent=2))
    return 0 if result.status == "PUBLISHED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
