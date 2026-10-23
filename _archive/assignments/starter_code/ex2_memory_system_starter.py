"""Exercise 2.1: Type-Safe Handoffs for a Customer Service Crew.

This file intentionally uses a real business workflow instead of abstract
schemas. Three agents collaborate on a customer support transcript:

1. TranscriptAnalyzerAgent -> TranscriptAnalysis
2. QualityEvaluatorAgent -> QualityEvaluation
3. FinalReportAgent -> FinalReport

Run:
    python3 assignments/starter_code/ex2_memory_system_starter.py
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class StrictModel(BaseModel):
    """Reject extra fields so agent drift fails before downstream use."""

    model_config = ConfigDict(extra="forbid")


class TranscriptAnalysis(StrictModel):
    """Agent 1 output: raw customer text becomes structured operating data."""

    ticket_id: str
    customer_id: str
    issue_category: Literal["billing", "technical", "account", "shipping", "unknown"]
    sentiment: Literal["positive", "neutral", "frustrated", "angry"]
    urgency: Literal["low", "medium", "high", "critical"]
    key_facts: list[str] = Field(min_length=1)
    requested_resolution: str
    contains_pii: bool

    @field_validator("ticket_id", "customer_id")
    @classmethod
    def ids_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("IDs cannot be blank.")
        return value


class QualityEvaluation(StrictModel):
    """Agent 2 output: a QA gate before the final customer-facing response."""

    ticket_id: str
    approved: bool
    quality_score: float = Field(ge=0.0, le=1.0)
    missing_information: list[str] = Field(default_factory=list)
    policy_risks: list[str] = Field(default_factory=list)
    escalation_required: bool
    reason: str


class FinalReport(StrictModel):
    """Agent 3 output: final typed artifact for CRM, QA, or human review."""

    ticket_id: str
    summary: str
    recommended_action: Literal[
        "reply",
        "refund_review",
        "technical_escalation",
        "manager_escalation",
        "close",
    ]
    customer_response: str
    internal_notes: str
    audit_trail: list[str] = Field(min_length=1)


class TranscriptAnalyzerAgent:
    """Agent 1: Extract structured signal from a customer transcript."""

    def analyze(self, transcript: str, ticket_id: str, customer_id: str) -> TranscriptAnalysis:
        text = transcript.lower()
        issue_category: Literal["billing", "technical", "account", "shipping", "unknown"] = "unknown"
        if "charged" in text or "invoice" in text or "refund" in text:
            issue_category = "billing"
        elif "login" in text or "password" in text or "account" in text:
            issue_category = "account"
        elif "error" in text or "bug" in text or "not working" in text:
            issue_category = "technical"
        elif "shipment" in text or "delivery" in text:
            issue_category = "shipping"

        sentiment: Literal["positive", "neutral", "frustrated", "angry"] = "neutral"
        if "angry" in text or "unacceptable" in text:
            sentiment = "angry"
        elif "frustrated" in text or "upset" in text or "charged twice" in text:
            sentiment = "frustrated"
        elif "thanks" in text or "appreciate" in text:
            sentiment = "positive"

        urgency: Literal["low", "medium", "high", "critical"] = "medium"
        if "legal" in text or "breach" in text:
            urgency = "critical"
        elif sentiment in {"angry", "frustrated"} or "charged twice" in text:
            urgency = "high"
        elif issue_category == "unknown":
            urgency = "low"

        key_facts = []
        if "charged twice" in text:
            key_facts.append("Customer reports duplicate charge.")
        if "refund" in text:
            key_facts.append("Customer requests refund or billing review.")
        if "login" in text:
            key_facts.append("Customer reports login/account access issue.")
        if not key_facts:
            key_facts.append("Customer needs support follow-up.")

        return TranscriptAnalysis(
            ticket_id=ticket_id,
            customer_id=customer_id,
            issue_category=issue_category,
            sentiment=sentiment,
            urgency=urgency,
            key_facts=key_facts,
            requested_resolution="Billing investigation and clear next-step response.",
            contains_pii="@" in transcript or "phone" in text,
        )


class QualityEvaluatorAgent:
    """Agent 2: Check whether the analysis is complete and policy-safe."""

    def evaluate(self, analysis: TranscriptAnalysis) -> QualityEvaluation:
        missing_information = []
        policy_risks = []

        if analysis.issue_category == "billing" and "charge" not in " ".join(analysis.key_facts).lower():
            missing_information.append("Specific billing fact is missing.")
        if analysis.contains_pii:
            policy_risks.append("Transcript contains PII; avoid exposing it in customer response.")
        if analysis.urgency in {"high", "critical"}:
            policy_risks.append("High-urgency customer issue requires human-visible audit trail.")

        approved = not missing_information
        return QualityEvaluation(
            ticket_id=analysis.ticket_id,
            approved=approved,
            quality_score=0.92 if approved else 0.55,
            missing_information=missing_information,
            policy_risks=policy_risks,
            escalation_required=analysis.urgency in {"high", "critical"} or bool(policy_risks),
            reason="Analysis is complete." if approved else "Analysis is missing required details.",
        )


class FinalReportAgent:
    """Agent 3: Produce the validated final artifact from typed inputs."""

    def compile(self, analysis: TranscriptAnalysis, evaluation: QualityEvaluation) -> FinalReport:
        if analysis.ticket_id != evaluation.ticket_id:
            raise ValueError("Ticket IDs do not match across handoff schemas.")

        if evaluation.escalation_required and analysis.issue_category == "billing":
            action = "refund_review"
        elif evaluation.escalation_required:
            action = "manager_escalation"
        elif analysis.issue_category == "technical":
            action = "technical_escalation"
        else:
            action = "reply"

        return FinalReport(
            ticket_id=analysis.ticket_id,
            summary=f"{analysis.issue_category.title()} issue with {analysis.sentiment} sentiment.",
            recommended_action=action,
            customer_response=(
                "Thanks for contacting us. We are reviewing the duplicate charge "
                "and will follow up with a clear resolution path."
            ),
            internal_notes=(
                f"Urgency={analysis.urgency}; score={evaluation.quality_score}; "
                f"risks={evaluation.policy_risks or ['none']}."
            ),
            audit_trail=[
                "TranscriptAnalyzerAgent produced TranscriptAnalysis.",
                "QualityEvaluatorAgent produced QualityEvaluation.",
                "FinalReportAgent produced FinalReport.",
            ],
        )


def run_customer_service_crew() -> FinalReport:
    transcript = (
        "I am frustrated because I was charged twice for my subscription. "
        "Please refund the duplicate charge. My email is customer@example.com."
    )

    analyzer = TranscriptAnalyzerAgent()
    evaluator = QualityEvaluatorAgent()
    reporter = FinalReportAgent()

    analysis = analyzer.analyze(transcript, ticket_id="TICK-2048", customer_id="CUST-991")
    evaluation = evaluator.evaluate(analysis)
    report = reporter.compile(analysis, evaluation)

    print("TranscriptAnalysis JSON:")
    print(analysis.model_dump_json(indent=2))
    print("\nQualityEvaluation JSON:")
    print(evaluation.model_dump_json(indent=2))
    print("\nFinalReport JSON:")
    print(report.model_dump_json(indent=2))

    return report


def demo_invalid_output_rejected() -> None:
    print("\nInvalid output rejection demo:")
    try:
        TranscriptAnalysis.model_validate(
            {
                "ticket_id": "TICK-BAD",
                "customer_id": "CUST-BAD",
                "issue_category": "billing",
                "sentiment": "furious",
                "urgency": "super urgent",
                "key_facts": [],
                "requested_resolution": "refund",
                "contains_pii": False,
                "hallucinated_field": "this should be rejected",
            }
        )
    except ValidationError as exc:
        for error in exc.errors():
            print(f"- {error['loc']}: {error['msg']}")


if __name__ == "__main__":
    final_report = run_customer_service_crew()
    assert final_report.recommended_action == "refund_review"
    demo_invalid_output_rejected()
