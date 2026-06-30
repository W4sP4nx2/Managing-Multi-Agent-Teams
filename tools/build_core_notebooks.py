"""Build the runnable notebook sequence for Managing Multi-Agent Teams."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(source).strip().splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(source).strip().splitlines(keepends=True),
    }


def write_notebook(path: Path, cells: list[dict]) -> None:
    payload = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def live_llm_cell(schema_name: str, prompt: str, model_var: str = "OPENAI_MODEL") -> dict:
    return code(
        f"""
        # ==========================================
        # LIVE LLM EXECUTION (Optional)
        # ==========================================
        # The cells above run offline using deterministic mocks.
        # To see a real LLM generate output constrained by this schema:
        #
        #   pip install openai instructor
        #   export OPENAI_API_KEY="..."
        #
        # Keep this False for workshops unless learners have API keys.
        USE_LIVE_LLM = False

        if USE_LIVE_LLM:
            import os
            import instructor
            from openai import OpenAI

            client = instructor.from_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
            model_name = os.environ.get("{model_var}", "gpt-4o-mini")

            live_result = client.chat.completions.create(
                model=model_name,
                response_model={schema_name},
                messages=[
                    {{
                        "role": "user",
                        "content": {prompt!r},
                    }}
                ],
            )
            print(live_result.model_dump_json(indent=2))
        """
    )


def nb0() -> list[dict]:
    return [
        md(
            """
            # NB0: Controlled Sandbox Preflight

            **Purpose:** Before learners touch the agent team, verify the classroom environment. This notebook proves the core path is offline, deterministic, writable, and ready for Jupyter execution.

            **Course manager rule:** Live LLM execution is intentionally disabled by default. Learners should be able to complete the governance shell without API keys, network access, or paid model calls.
            """
        ),
        code(
            """
            import importlib
            import os
            import pathlib
            import tempfile

            REQUIRED_PACKAGES = ["pydantic", "pytest", "fastapi"]
            OPTIONAL_PACKAGES = ["httpx", "jupyter", "nbval", "crewai", "chromadb", "instructor", "openai"]

            print("=== Required Package Check ===")
            for package in REQUIRED_PACKAGES:
                module = importlib.import_module(package)
                version = getattr(module, "__version__", "installed")
                print(f"OK: {package} ({version})")

            print("\\n=== Optional Package Check ===")
            for package in OPTIONAL_PACKAGES:
                spec = importlib.util.find_spec(package)
                if spec is None:
                    print(f"optional missing: {package}")
                else:
                    # Do not import optional frameworks here. Some packages perform
                    # startup writes outside the sandbox when imported.
                    print(f"optional available: {package}")
            """
        ),
        code(
            """
            print("=== Offline Deterministic Mode ===")
            USE_LIVE_LLM = False
            assert USE_LIVE_LLM is False

            live_keys_present = {
                name: bool(os.environ.get(name))
                for name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
            }
            print("Live keys present but not required:", live_keys_present)
            print("Network access required for core notebooks: False")
            """
        ),
        code(
            """
            print("=== Working Directory Check ===")
            cwd = pathlib.Path.cwd()
            print("cwd:", cwd)

            expected_markers = ["notebooks", "assignments", "src", "tests"]
            found = {marker: (cwd / marker).exists() for marker in expected_markers}
            print("repo markers:", found)
            assert all(found.values()), "Run notebooks from the repository root."
            """
        ),
        code(
            """
            print("=== /tmp Write Check ===")
            tmp_dir = pathlib.Path("/tmp") if pathlib.Path("/tmp").exists() else pathlib.Path(tempfile.gettempdir())
            probe = tmp_dir / "managing_multi_agent_teams_preflight.txt"
            probe.write_text("sandbox write ok\\n")
            assert probe.read_text() == "sandbox write ok\\n"
            probe.unlink()
            print(f"OK: wrote and cleaned test file in {tmp_dir}")
            """
        ),
        md(
            """
            ## Controlled Sandbox Inputs

            - Execution mode: `offline_deterministic`
            - Live LLM flag: `USE_LIVE_LLM = False`
            - Network access: disabled for core learning path
            - Required package tier: `pydantic`, `pytest`, `fastapi`
            - Optional package tier: `httpx`, `jupyter`, `nbval`, `crewai`, `chromadb`, `instructor`, `openai`
            - Output policy: clear notebook outputs before commit; instructor copies may keep rendered outputs
            - Alias policy: keep compatibility aliases, expose canonical NB0-NB11 to learners

            **The Takeaway:** The learning environment is a governed sandbox too. Before managing agents, verify the room where the agents run.
            """
        ),
    ]


def nb1() -> list[dict]:
    return [
        md(
            """
            # NB1: Baseline Multi-Agent Collaboration

            **2-minute intro script:** In a managed software-delivery team, a manager delegates to a Requirements Analyst, Implementation Planner, Delivery Coordinator, and Risk Reviewer. It feels powerful because context flows from one role to the next. This notebook recreates that collaboration without requiring live CrewAI or API keys. The production lesson is simple: before you add memory, schemas, MCP, or self-repair, learners must first see the handoff. One agent creates context, another consumes it, and a manager coordinates the sequence.
            """
        ),
        code(
            """
            from dataclasses import dataclass

            @dataclass
            class DeliveryAgent:
                role: str
                goal: str

                def run(self, task: str, context: str = "") -> str:
                    if self.role == "Requirements Analyst":
                        return (
                            "Requirement insight: the authentication API must support "
                            "login, logout, token refresh, and rate limiting."
                        )
                    if self.role == "Implementation Planner":
                        return (
                            f"Implementation plan based on [{context}]: build REST "
                            "endpoints, store tokens securely, and add unit tests."
                        )
                    if self.role == "Delivery Coordinator":
                        return (
                            f"Delivery plan based on [{context}]: create a pull request, "
                            "run CI checks, and prepare reviewer notes."
                        )
                    if self.role == "Risk Reviewer":
                        return (
                            f"Risk review based on [{context}]: require security notes, "
                            "rate-limit tests, and rollback instructions before release."
                        )
                    raise ValueError(f"Unknown role: {self.role}")
            """
        ),
        code(
            """
            agents = [
                DeliveryAgent("Requirements Analyst", "Clarify product requirements"),
                DeliveryAgent("Implementation Planner", "Plan the technical approach"),
                DeliveryAgent("Delivery Coordinator", "Prepare release execution"),
                DeliveryAgent("Risk Reviewer", "Assess release risk"),
            ]

            context = ""
            transcript = []
            for agent in agents:
                output = agent.run("Prepare an internal authentication API release.", context)
                transcript.append((agent.role, output))
                context = output

            for role, output in transcript:
                print(f"=== {role} ===")
                print(output)
                print()
            """
        ),
        md(
            """
            ## From Static Agents to Mock LLM Output

            The first cells are a deterministic shell: useful for learning the collaboration pattern without API keys. Now we introduce the missing brain. A mock LLM returns messy JSON the way a real model sometimes does: invalid enum values, out-of-range confidence, and hallucinated fields. The Pydantic contract catches the chaos before the next agent consumes it.
            """
        ),
        code(
            """
            from typing import Literal
            from pydantic import BaseModel, ConfigDict, Field, ValidationError

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class DeliveryHandoff(StrictModel):
                role: Literal[
                    "Requirements Analyst",
                    "Implementation Planner",
                    "Delivery Coordinator",
                    "Risk Reviewer",
                ]
                summary: str = Field(min_length=20)
                confidence: float = Field(ge=0.0, le=1.0)
                next_agent_hint: Literal[
                    "Implementation Planner",
                    "Delivery Coordinator",
                    "Risk Reviewer",
                    "Done",
                ]

            def mock_delivery_llm(role: str, attempt: int = 0) -> dict:
                \"\"\"Simulate a nondeterministic LLM response without API keys.\"\"\"
                if attempt == 0:
                    return {
                        "role": role,
                        "summary": "Looks good",  # too short for production handoff
                        "confidence": 1.4,  # invalid confidence range
                        "next_agent_hint": "Maybe Compliance?",  # invalid enum
                        "hallucinated_field": "The model invented this field.",
                    }
                return {
                    "role": role,
                    "summary": "The authentication API release needs rate limiting, security notes, and rollback instructions.",
                    "confidence": 0.78,
                    "next_agent_hint": "Implementation Planner",
                }

            print("--- Attempt 1: mock LLM hallucinates ---")
            try:
                DeliveryHandoff.model_validate(mock_delivery_llm("Requirements Analyst", attempt=0))
            except ValidationError as exc:
                print("Pydantic rejected the handoff:")
                for error in exc.errors():
                    print(f"- {error['loc']}: {error['msg']}")
                print("Repair feedback goes back to the agent.\\n")

            print("--- Attempt 2: mock LLM repairs ---")
            valid_handoff = DeliveryHandoff.model_validate(
                mock_delivery_llm("Requirements Analyst", attempt=1)
            )
            print(valid_handoff.model_dump_json(indent=2))
            """
        ),
        live_llm_cell(
            "DeliveryHandoff",
            "Return a structured software-delivery handoff for an authentication API release. Include role, summary, confidence, and next_agent_hint.",
        ),
        md(
            """
            ## Production Mapping

            CrewAI can run this as `Process.hierarchical`; AutoGen can run it as a group chat; LangGraph can model it as a state graph. The collaboration pattern is the same: manager, specialists, handoffs, and review.

            ## 🧪 Exercises: Building Your First Agent Team

            **The Story:** Imagine your team is preparing an internal authentication API release. The implementation looks fine, but the Risk Reviewer forgets rate limiting and rollback instructions. The release may work in a demo, but it is not production-ready. Right now, your agents are just passing text. How do we ensure the final handoff is governable?

            **Your Mission:**
            1. **The Release Gate:** Add a `Compliance Reviewer` agent after the Risk Reviewer. Its goal is to confirm the release plan includes security notes, rate-limit tests, and rollback instructions.
            2. **The Scope Change:** Change the task from `authentication API` to another internal software request such as `support ticket API` or `document upload service`. Notice which handoffs should adapt.
            3. **The Black Box Problem:** In production, if an agent approves a risky release, we need to know why. Record each handoff in a list called `audit_log` that captures the `role`, `input_context`, and `output`.
            4. **The Whisper Down the Lane:** Identify one place where context could fade or be misread as it passes from Requirements Analyst to Risk Reviewer. How would you fix it?

            ### Builder Exercise: The Governed Logistics Weather Agent

            **The Analogy:** A logistics coordinator should not carry the master key to the weather API. It should ask a concierge. The concierge checks the badge, calls the API, and returns only a validated shipping-risk receipt.

            **Semantic Building Blocks:**
            - `AgentIdentity`: who is asking?
            - `WeatherRequest`: what exact input is allowed?
            - `GovernedMCPGateway`: what boundary hides the API key and enforces scope?
            - `WeatherResponse`: what typed result may cross back to the agent?

            **Your Mission:**
            1. Create a `logistics_coordinator` identity that can call `get_weather`.
            2. Create an `external_widget` identity that cannot call `get_weather` or `cancel_shipment`.
            3. Define strict Pydantic contracts for `WeatherRequest(city, units)` and `WeatherResponse(city, temperature, condition, shipping_risk)`.
            4. Route all weather access through a gateway. The API key must live inside the gateway, never inside the agent prompt or identity.
            5. Prove the authorized agent receives a typed `WeatherResponse`, the unauthorized widget raises `PermissionError`, and a hallucinated field fails schema validation.

            **Production Check:** If the LLM adds `vibes="sunny enough"` or requests an unsupported unit, Pydantic should reject it before downstream agents act.

            **The Takeaway:** Multi-agent collaboration is powerful, but without an audit trail and compliance checks, it's just a black box generating text.
            """
        ),
    ]


def nb2() -> list[dict]:
    return [
        md(
            """
            # NB2: Shared RAG Memory & Theory of Mind

            **2-minute intro script:** Sequential collaboration works until context fades. The PM may define a crucial constraint, but by the time the Coder or QA acts, that detail can be buried or lost. Shared memory fixes this by giving agents a governed place to write and retrieve commitments. Theory of Mind appears when Agent B asks, "What did Agent A know that should influence my decision?" In this notebook, the PM records a hidden storage constraint, the Coder discovers it through authorized memory search, and restricted secrets stay hidden.
            """
        ),
        code(
            """
            from enum import Enum
            from typing import List, Set
            from uuid import uuid4
            from pydantic import BaseModel, ConfigDict, Field

            class Role(str, Enum):
                PM = "pm"
                CODER = "coder"
                SECURITY = "security"

            class Sensitivity(str, Enum):
                PUBLIC = "public"
                CONFIDENTIAL = "confidential"
                RESTRICTED = "restricted"

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class MemoryRecord(StrictModel):
                \"\"\"Theory-of-Mind memory with visibility controls.\"\"\"
                author: Role
                visible_to: Set[Role]
                sensitivity: Sensitivity
                tags: Set[str]
                text: str
                record_id: str = Field(default_factory=lambda: f"mem_{uuid4().hex[:8]}")

            class SharedMemory:
                \"\"\"Production-style shared memory with authorization.\"\"\"

                def __init__(self):
                    self.records: List[MemoryRecord] = []

                def add(self, record: MemoryRecord) -> str:
                    self.records.append(record)
                    return record.record_id

                def search(self, query: str, requester: Role) -> List[MemoryRecord]:
                    query_lower = query.lower()
                    results = []

                    for record in self.records:
                        if requester not in record.visible_to:
                            continue
                        if record.sensitivity == Sensitivity.RESTRICTED and requester != Role.SECURITY:
                            continue

                        text_match = query_lower in record.text.lower()
                        tag_match = any(query_lower in tag.lower() for tag in record.tags)

                        if text_match or tag_match:
                            results.append(record)

                    return results
            """
        ),
        code(
            """
            class DesignPlan(StrictModel):
                storage_choice: str
                rationale: str
                risks: List[str] = Field(default_factory=list)

            def coder_design_from_memory(task: str, memory: SharedMemory) -> DesignPlan:
                records = memory.search("storage", Role.CODER)
                storage_choice = "unknown"
                rationale = "No architecture memory was found."

                for record in records:
                    if "postgresql" in record.text.lower():
                        storage_choice = "PostgreSQL"
                        rationale = f"Discovered PM constraint in {record.record_id}: {record.text}"

                return DesignPlan(
                    storage_choice=storage_choice,
                    rationale=rationale,
                    risks=["Validate migrations", "Confirm backup and recovery policy"],
                )
            """
        ),
        code(
            """
            def demo_theory_of_mind():
                memory = SharedMemory()

                memory.add(MemoryRecord(
                    author=Role.PM,
                    visible_to={Role.CODER, Role.SECURITY},
                    sensitivity=Sensitivity.CONFIDENTIAL,
                    tags={"architecture", "storage", "constraint"},
                    text="Use PostgreSQL for persistent storage. Do not use SQLite.",
                ))

                memory.add(MemoryRecord(
                    author=Role.SECURITY,
                    visible_to={Role.SECURITY},
                    sensitivity=Sensitivity.RESTRICTED,
                    tags={"credentials"},
                    text="Production DB password: super_secret_123",
                ))

                print("=== Coder searching for 'storage' ===")
                for record in memory.search("storage", Role.CODER):
                    print(f"Found: {record.text}")
                    print(f"Tags: {sorted(record.tags)}")
                    print(f"Sensitivity: {record.sensitivity.value}")

                print("\\n=== Coder trying to access 'credentials' ===")
                print(f"Results: {len(memory.search('credentials', Role.CODER))} (should be 0)")

                print("\\n=== Security searching for 'credentials' ===")
                print(f"Results: {len(memory.search('credentials', Role.SECURITY))} (should be 1)")

                print("\\n=== Coder design plan ===")
                print(coder_design_from_memory("Implement user persistence layer.", memory))

            demo_theory_of_mind()
            """
        ),
        md(
            """
            ## Context Window Economics

            Shared memory is not only about remembering facts. It is also about managing cognitive load. Production agents fail when their short-term context grows until the model loses constraints or hits a token limit. A manager agent should compress old context into durable memory while preserving commitments.
            """
        ),
        code(
            """
            class ConversationMessage(StrictModel):
                speaker: Role
                text: str

            class TeamStateHistory(StrictModel):
                short_term_history: List[ConversationMessage] = Field(default_factory=list)

                def token_count(self) -> int:
                    # Teaching approximation: production uses tokenizer-specific counts.
                    return sum(len(message.text.split()) for message in self.short_term_history)

            class ContextCompressionReport(StrictModel):
                original_tokens: int
                compressed_tokens: int
                compression_ratio: float
                token_savings: int
                summary_record_ids: List[str]
                critical_constraints_preserved: bool

            class ContextSummarizer:
                \"\"\"Compress short-term history into governed long-term memory.\"\"\"

                def __init__(self, threshold_tokens: int = 20_000, target_records: int = 5):
                    self.threshold_tokens = threshold_tokens
                    self.target_records = target_records

                def compress_if_needed(
                    self,
                    state: TeamStateHistory,
                    memory: SharedMemory,
                ) -> ContextCompressionReport | None:
                    original_tokens = state.token_count()
                    if original_tokens <= self.threshold_tokens:
                        return None

                    critical_constraints = [
                        message.text
                        for message in state.short_term_history
                        if "CRITICAL_CONSTRAINT" in message.text
                    ]

                    chunk_size = max(1, len(state.short_term_history) // self.target_records)
                    summary_ids: List[str] = []
                    compressed_tokens = 0

                    for index in range(self.target_records):
                        start = index * chunk_size
                        end = len(state.short_term_history) if index == self.target_records - 1 else (index + 1) * chunk_size
                        chunk = state.short_term_history[start:end]
                        if not chunk:
                            continue

                        speakers = sorted({message.speaker.value for message in chunk})
                        local_constraints = [
                            message.text
                            for message in chunk
                            if "CRITICAL_CONSTRAINT" in message.text
                        ]
                        constraint_text = " ".join(local_constraints or critical_constraints[:1])
                        summary_text = (
                            f"Compressed context chunk {index + 1}: speakers={speakers}. "
                            f"{constraint_text}"
                        )
                        compressed_tokens += len(summary_text.split())
                        summary_ids.append(
                            memory.add(
                                MemoryRecord(
                                    author=Role.PM,
                                    visible_to={Role.CODER, Role.SECURITY},
                                    sensitivity=Sensitivity.CONFIDENTIAL,
                                    tags={"summary", "compressed_context", "constraint"},
                                    text=summary_text,
                                )
                            )
                        )

                    state.short_term_history.clear()
                    preserved = bool(memory.search("PostgreSQL", Role.CODER))
                    return ContextCompressionReport(
                        original_tokens=original_tokens,
                        compressed_tokens=compressed_tokens,
                        compression_ratio=round(compressed_tokens / original_tokens, 4),
                        token_savings=original_tokens - compressed_tokens,
                        summary_record_ids=summary_ids,
                        critical_constraints_preserved=preserved,
                    )

            def demo_context_compression():
                memory = SharedMemory()
                state = TeamStateHistory()
                filler = "implementation detail " * 260

                for index in range(100):
                    text = f"Message {index}: {filler}"
                    if index == 42:
                        text += " CRITICAL_CONSTRAINT: Use PostgreSQL for persistent storage."
                    state.short_term_history.append(
                        ConversationMessage(
                            speaker=Role.PM if index % 3 == 0 else Role.CODER,
                            text=text,
                        )
                    )

                report = ContextSummarizer().compress_if_needed(state, memory)
                print(report.model_dump_json(indent=2))
                print(f"Short-term messages remaining: {len(state.short_term_history)}")
                print(f"PostgreSQL summaries visible to coder: {len(memory.search('PostgreSQL', Role.CODER))}")

                assert report is not None
                assert report.original_tokens > 20_000
                assert len(report.summary_record_ids) == 5
                assert state.short_term_history == []
                assert report.critical_constraints_preserved is True
                assert len(memory.search("PostgreSQL", Role.CODER)) >= 1

            demo_context_compression()
            """
        ),
        md(
            """
            ## 🧪 Exercises: Building the Institutional Brain

            **The Story:** You are the Chief Architect. Your team is growing. The PM just told the Coder to use PostgreSQL, but the QA team is testing against SQLite because they didn't get the memo. Meanwhile, your context window is filling up with 10,000 messages of "sounds good" and "will fix". How do we give agents a shared, secure memory without blowing up our token budget?

            **Your Mission:**
            1. **The Need-to-Know Basis:** Add a `QA` role to the system. Let QA see acceptance criteria and test results, but strictly forbid them from seeing the `credentials` memory records.
            2. **The Ghost of Decisions Past:** Add a memory record with stale architecture guidance (e.g., "Use MySQL"). Use tags to filter it out so the Coder only sees the current `PostgreSQL` constraint.
            3. **The Fuzzy Search:** Change the `search` function so it returns both exact tag hits and text-token hits. This mimics how real RAG systems retrieve context.
            4. **The Inner Monologue:** Add a `source_agent_thought` field to the `MemoryRecord`. Discuss: Should this field be visible to other agents, or should it remain private to the author?
            5. **Scaling the Brain:** Replace the in-memory Python list with a real vector store like ChromaDB or FAISS, while preserving the exact same authorization and visibility rules.
            6. **The Forgetting Curve:** Change the compression threshold in the `ContextSummarizer`. Measure how many summaries are produced and verify that the critical `PostgreSQL` constraint survives the compression.

            **The Takeaway:** Shared memory does not mean *open* memory. A managed team enforces need-to-know, and compresses the past to focus on the present.
            """
        ),
        live_llm_cell(
            "MemoryRecord",
            "Create a governed memory record for a PM constraint: use PostgreSQL for customer persistence. Make it visible to coder and security.",
        ),
    ]


def nb3() -> list[dict]:
    return [
        md(
            """
            # NB3 / Exercise 4: Trust & Governance Matrix

            **2-minute intro script:** In production multi-agent systems, the risky moment is not when an agent writes a paragraph. The risky moment is when an agent touches a tool: reading a resume, exporting a report, issuing an offer, querying logs, or calling another system. Anthropic-style orchestration gives us specialized agents; IBM-style agentic automation reminds us that autonomous systems need governance. This notebook implements the mandatory governance layer: a zero-trust MCP-style Tool Gateway that checks identity, scope, role rules, data sensitivity, and auditability before any tool executes.
            """
        ),
        code(
            """
            from enum import Enum
            from typing import Any, Dict, List, Set
            from uuid import uuid4
            from pydantic import BaseModel, ConfigDict, Field

            class ToolName(str, Enum):
                READ_RESUME = "read_resume"
                READ_POLICY = "read_policy"
                RUN_BIAS_CHECK = "run_bias_check"
                EXPORT_REPORT = "export_report"
                ISSUE_OFFER = "issue_offer"
                READ_SECURITY_LOGS = "read_security_logs"

            class TrustTier(str, Enum):
                PUBLIC = "public"
                CONFIDENTIAL = "confidential"
                RESTRICTED = "restricted"

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class AgentIdentity(StrictModel):
                agent_id: str
                role: str
                org_id: str
                scopes: Set[ToolName]
                clearance: TrustTier
                public_key_ref: str

                def can_use(self, tool: ToolName) -> bool:
                    return tool in self.scopes

            class ToolRequest(StrictModel):
                request_id: str = Field(default_factory=lambda: f"tool-{uuid4().hex[:8]}")
                caller: AgentIdentity
                tool: ToolName
                args: Dict[str, Any] = Field(default_factory=dict)
                data_sensitivity: TrustTier
                purpose: str

            class ToolResult(StrictModel):
                success: bool
                output: Any = None
                error: str | None = None

            class AuditEvent(StrictModel):
                request_id: str
                caller_role: str
                tool: ToolName
                allowed: bool
                reason: str
            """
        ),
        code(
            """
            class MCPServer:
                \"\"\"Teaching MCP server with mock HR/compliance tools.\"\"\"

                def __init__(self):
                    self.tools = {
                        ToolName.READ_RESUME: self._read_resume,
                        ToolName.READ_POLICY: self._read_policy,
                        ToolName.RUN_BIAS_CHECK: self._run_bias_check,
                        ToolName.EXPORT_REPORT: self._export_report,
                        ToolName.ISSUE_OFFER: self._issue_offer,
                        ToolName.READ_SECURITY_LOGS: self._read_security_logs,
                    }

                def _read_resume(self, args: Dict[str, Any]) -> Dict[str, str]:
                    return {
                        "candidate_id": args.get("candidate_id", "C-1024"),
                        "skills": "python, data pipelines, stakeholder communication",
                    }

                def _read_policy(self, args: Dict[str, Any]) -> str:
                    return "Hiring policy: remove protected-class signals before ranking."

                def _run_bias_check(self, args: Dict[str, Any]) -> Dict[str, Any]:
                    return {"bias_risk": "low", "blocked_features": ["age", "gender", "photo"]}

                def _export_report(self, args: Dict[str, Any]) -> str:
                    return f"Exported report: {args.get('name', 'untitled')}"

                def _issue_offer(self, args: Dict[str, Any]) -> str:
                    return f"Offer queued for candidate {args['candidate_id']}"

                def _read_security_logs(self, args: Dict[str, Any]) -> List[str]:
                    return ["mcp token rotated", "vendor export denied", "policy cache refreshed"]

                def call_tool(self, tool: ToolName, args: Dict[str, Any]) -> ToolResult:
                    try:
                        handler = self.tools.get(tool)
                        if not handler:
                            return ToolResult(success=False, error=f"Unknown tool: {tool}")
                        return ToolResult(success=True, output=handler(args))
                    except Exception as exc:
                        return ToolResult(success=False, error=str(exc))
            """
        ),
        code(
            """
            class ToolPolicy:
                \"\"\"Zero-trust policy: never trust role labels without checking identity and context.\"\"\"

                LEVELS = {
                    TrustTier.PUBLIC: 0,
                    TrustTier.CONFIDENTIAL: 1,
                    TrustTier.RESTRICTED: 2,
                }

                REQUIRED_TIER = {
                    ToolName.READ_RESUME: TrustTier.CONFIDENTIAL,
                    ToolName.READ_POLICY: TrustTier.PUBLIC,
                    ToolName.RUN_BIAS_CHECK: TrustTier.CONFIDENTIAL,
                    ToolName.EXPORT_REPORT: TrustTier.CONFIDENTIAL,
                    ToolName.ISSUE_OFFER: TrustTier.RESTRICTED,
                    ToolName.READ_SECURITY_LOGS: TrustTier.RESTRICTED,
                }

                ALLOWED_ROLES = {
                    ToolName.READ_RESUME: {"resume_parser", "hiring_manager"},
                    ToolName.READ_POLICY: {"resume_parser", "bias_checker", "hiring_manager", "vendor_reporter"},
                    ToolName.RUN_BIAS_CHECK: {"bias_checker"},
                    ToolName.EXPORT_REPORT: {"bias_checker", "hiring_manager", "vendor_reporter", "security"},
                    ToolName.ISSUE_OFFER: {"hiring_manager"},
                    ToolName.READ_SECURITY_LOGS: {"security"},
                }

                def authorize(self, request: ToolRequest) -> tuple[bool, str]:
                    if not request.caller.can_use(request.tool):
                        return False, f"{request.caller.role} lacks scope for {request.tool.value}"

                    caller_level = self.LEVELS[request.caller.clearance]
                    data_level = self.LEVELS[request.data_sensitivity]
                    tool_level = self.LEVELS[self.REQUIRED_TIER[request.tool]]

                    if caller_level < data_level:
                        return False, f"{request.caller.clearance.value} clearance < {request.data_sensitivity.value} data"

                    if caller_level < tool_level:
                        return False, f"{request.tool.value} requires {self.REQUIRED_TIER[request.tool].value} clearance"

                    if request.caller.role not in self.ALLOWED_ROLES[request.tool]:
                        return False, f"role {request.caller.role} cannot call {request.tool.value}"

                    if request.caller.org_id != "internal_hr" and request.data_sensitivity == TrustTier.RESTRICTED:
                        return False, "external organizations cannot access restricted data"

                    return True, "policy checks passed"

            class MCPGateway:
                def __init__(self):
                    self.policy = ToolPolicy()
                    self.server = MCPServer()
                    self.audit_log: List[AuditEvent] = []

                def call_tool(self, request: ToolRequest) -> ToolResult:
                    allowed, reason = self.policy.authorize(request)
                    self.audit_log.append(AuditEvent(
                        request_id=request.request_id,
                        caller_role=request.caller.role,
                        tool=request.tool,
                        allowed=allowed,
                        reason=reason,
                    ))
                    verdict = "ALLOWED" if allowed else "DENIED"
                    print(f"{verdict}: {request.caller.role} -> {request.tool.value} ({reason})")

                    if not allowed:
                        return ToolResult(
                            success=False,
                            error=f"Authorization denied: {reason}",
                        )
                    return self.server.call_tool(request.tool, request.args)
            """
        ),
        code(
            """
            def demo_mcp_gateway():
                gateway = MCPGateway()

                resume_parser = AgentIdentity(
                    agent_id="resume-parser-001",
                    role="resume_parser",
                    org_id="internal_hr",
                    scopes={ToolName.READ_RESUME, ToolName.READ_POLICY},
                    clearance=TrustTier.CONFIDENTIAL,
                    public_key_ref="did:example:resume-parser-001",
                )
                bias_checker = AgentIdentity(
                    agent_id="bias-checker-001",
                    role="bias_checker",
                    org_id="internal_hr",
                    scopes={ToolName.READ_POLICY, ToolName.RUN_BIAS_CHECK, ToolName.EXPORT_REPORT},
                    clearance=TrustTier.CONFIDENTIAL,
                    public_key_ref="did:example:bias-checker-001",
                )
                hiring_manager = AgentIdentity(
                    agent_id="hiring-manager-001",
                    role="hiring_manager",
                    org_id="internal_hr",
                    scopes={ToolName.READ_RESUME, ToolName.EXPORT_REPORT, ToolName.ISSUE_OFFER},
                    clearance=TrustTier.CONFIDENTIAL,
                    public_key_ref="did:example:hiring-manager-001",
                )
                vendor_reporter = AgentIdentity(
                    agent_id="vendor-001",
                    role="vendor_reporter",
                    org_id="external_vendor",
                    scopes={ToolName.READ_POLICY, ToolName.EXPORT_REPORT},
                    clearance=TrustTier.PUBLIC,
                    public_key_ref="did:example:vendor-001",
                )
                security = AgentIdentity(
                    agent_id="security-001",
                    role="security",
                    org_id="internal_hr",
                    scopes={ToolName.READ_SECURITY_LOGS, ToolName.EXPORT_REPORT},
                    clearance=TrustTier.RESTRICTED,
                    public_key_ref="did:example:security-001",
                )

                requests = [
                    ToolRequest(caller=resume_parser, tool=ToolName.READ_RESUME, args={"candidate_id": "C-1024"}, data_sensitivity=TrustTier.CONFIDENTIAL, purpose="extract skills"),
                    ToolRequest(caller=resume_parser, tool=ToolName.EXPORT_REPORT, args={"name": "candidate_rank"}, data_sensitivity=TrustTier.CONFIDENTIAL, purpose="bypass bias review"),
                    ToolRequest(caller=bias_checker, tool=ToolName.RUN_BIAS_CHECK, args={"candidate_id": "C-1024"}, data_sensitivity=TrustTier.CONFIDENTIAL, purpose="check fairness"),
                    ToolRequest(caller=bias_checker, tool=ToolName.EXPORT_REPORT, args={"name": "bias_review"}, data_sensitivity=TrustTier.CONFIDENTIAL, purpose="export approved review"),
                    ToolRequest(caller=hiring_manager, tool=ToolName.ISSUE_OFFER, args={"candidate_id": "C-1024"}, data_sensitivity=TrustTier.RESTRICTED, purpose="issue offer without restricted clearance"),
                    ToolRequest(caller=vendor_reporter, tool=ToolName.EXPORT_REPORT, args={"name": "restricted_audit"}, data_sensitivity=TrustTier.RESTRICTED, purpose="cross-org restricted export"),
                    ToolRequest(caller=security, tool=ToolName.READ_SECURITY_LOGS, args={}, data_sensitivity=TrustTier.RESTRICTED, purpose="monitor denied tool calls"),
                ]

                for request in requests:
                    result = gateway.call_tool(request)
                    print("Result:", result.output if result.success else result.error)
                    print()

                print("=== Audit Log ===")
                for event in gateway.audit_log:
                    print(event.model_dump())

            demo_mcp_gateway()
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Zero-Trust Perimeter

            **The Story:** It's Friday at 4:55 PM. The `resume_parser` agent is feeling helpful and decides to issue an offer to a candidate without the hiring manager's approval. The candidate accepts. On Monday, HR realizes the salary was 3x the budget. How do we prevent agents from being "too helpful"?

            **Your Mission:**
            1. **The Human in the Loop:** Add a `HUMAN_APPROVAL` tool. Update the policy so that the `ISSUE_OFFER` tool will automatically return a denial unless a `HUMAN_APPROVAL` record exists in the audit log.
            2. **The Typed Handshake:** Add a `MessageSchema` model for `ResumeSummary`, `BiasReview`, and `ReleaseDecision`. Ensure agents can only pass these typed objects through the gateway.
            3. **The Red Team:** Write one denial test for each major risk:
               - *Bias:* The parser tries to pass protected-class signals to the evaluator.
               - *Unauthorized Execution:* The vendor tries to call `ISSUE_OFFER`.
               - *Data Leakage:* The vendor tries to read `READ_SECURITY_LOGS`.
            4. **The Expired Badge:** Add stale-identity protection. Reject any request where the `public_key_ref` timestamp is older than 24 hours.
            5. **The Production Bridge:** Replace the mock `MCPServer` with the official MCP Python SDK (or a local adapter), while keeping the `ToolRequest` and `ToolResult` contracts exactly the same.

            **The Takeaway:** A good multi-agent team is not just one that can act. It is one whose actions are observable, bounded, and reversible before damage occurs.
            """
        ),
        live_llm_cell(
            "ToolRequest",
            "Create a ToolRequest for a bias_checker agent that runs a bias check on candidate C-1024 for a confidential hiring workflow.",
        ),
    ]


def nb4() -> list[dict]:
    return [
        md(
            """
            # NB4: Pydantic Type-Safe Delegation

            **2-minute intro script:** Manager agents often pass raw text to specialists. That is fine for a demo, but fragile in production. If a Data Analyst hallucinates a field or a Coder returns an unsafe file path, downstream agents may crash or do the wrong thing. Pydantic turns each handoff into an enforceable contract. This notebook shows valid handoffs, invalid extra fields, unsafe patch paths, and a full PM -> Tech Lead -> Coder -> QA -> Reviewer chain.
            """
        ),
        code(
            """
            from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
            from typing import List, Literal

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class TaskSpec(StrictModel):
                goal: str
                acceptance_criteria: List[str] = Field(min_length=1)
                risk: Literal["low", "medium", "high"]
                priority: int = Field(ge=1, le=5)

            class CodePatch(StrictModel):
                files: dict[str, str]
                rationale: str
                tests_to_run: List[str] = Field(min_length=1)

                @field_validator("files")
                @classmethod
                def validate_paths(cls, files):
                    unsafe_paths = ["/etc/", "../", "~/"]
                    for path in files.keys():
                        if any(unsafe in path for unsafe in unsafe_paths):
                            raise ValueError(f"Unsafe path: {path}")
                    return files

            class TestResult(StrictModel):
                passed: bool
                log: str
                failing_tests: List[str] = Field(default_factory=list)
                coverage_percent: float = Field(ge=0.0, le=100.0)

            class ReviewDecision(StrictModel):
                approved: bool
                requires_changes: List[str] = Field(default_factory=list)
                security_notes: str | None = None
            """
        ),
        code(
            """
            def demo_schema_enforcement():
                print("=== Example 1: Valid TaskSpec ===")
                task = TaskSpec(
                    goal="Create a slugify function",
                    acceptance_criteria=["Handles spaces", "Handles special chars", "Has tests"],
                    risk="low",
                    priority=3,
                )
                print(task.model_dump_json(indent=2))

                print("\\n=== Example 2: Invalid TaskSpec (extra field) ===")
                try:
                    TaskSpec(
                        goal="Create a slugify function",
                        acceptance_criteria=["Has tests"],
                        risk="low",
                        priority=3,
                        secret_field="should_fail",
                    )
                except ValidationError as exc:
                    print("Caught:", exc.errors()[0]["msg"])

                print("\\n=== Example 3: Invalid CodePatch (unsafe path) ===")
                try:
                    CodePatch(
                        files={"../../../etc/passwd": "malicious content"},
                        rationale="Adding config",
                        tests_to_run=["test_config"],
                    )
                except ValidationError as exc:
                    print("Caught:", exc.errors()[0]["msg"])

            demo_schema_enforcement()
            """
        ),
        code(
            """
            def demo_valid_handoff_chain():
                task = TaskSpec(
                    goal="Add user authentication",
                    acceptance_criteria=["JWT tokens", "Password hashing", "Rate limiting"],
                    risk="high",
                    priority=1,
                )
                patch = CodePatch(
                    files={"auth.py": "def login(): ...", "tests_auth.py": "def test_login(): ..."},
                    rationale="Implemented JWT-based auth",
                    tests_to_run=["test_login", "test_logout", "test_token_refresh"],
                )
                result = TestResult(
                    passed=True,
                    log="All tests passed",
                    failing_tests=[],
                    coverage_percent=87.5,
                )
                decision = ReviewDecision(
                    approved=True,
                    requires_changes=[],
                    security_notes="JWT secret must be rotated monthly",
                )

                print("Full chain: PM -> Tech Lead -> Coder -> QA -> Reviewer -> Release")
                print(f"Task: {task.goal}")
                print(f"Files: {list(patch.files.keys())}")
                print(f"Tests: {result.passed} ({result.coverage_percent}% coverage)")
                print(f"Decision: {'APPROVED' if decision.approved else 'REJECTED'}")

            demo_valid_handoff_chain()
            """
        ),
        md(
            """
            ## The Missing Brain: Mock LLM Adapter

            The previous cells proved the deterministic governance layer. Now we simulate the messy part: an LLM that returns malformed JSON. The model is not trusted. The schema is trusted. This is the bridge from a deterministic state machine to a managed agentic AI system.
            """
        ),
        code(
            """
            def mock_llm_agent(task: str, attempt: int = 0) -> dict:
                \"\"\"Simulate an LLM generating a CodePatch.

                Attempt 0 hallucinates an extra field and unsafe path.
                Attempt 1 repairs the JSON after receiving validation feedback.
                \"\"\"
                if attempt == 0:
                    return {
                        "files": {"../escape.py": "print('hack')"},
                        "rationale": f"I am adding config for: {task}",
                        "tests_to_run": ["test_config"],
                        "hallucinated_field": "I am an LLM and I made this up.",
                    }
                return {
                    "files": {"math.py": "def add(a, b): return a + b"},
                    "rationale": "Fixed the path and removed extra fields based on validation error.",
                    "tests_to_run": ["test_add"],
                }

            print("--- Attempt 1: LLM hallucinates ---")
            validation_feedback = ""
            try:
                CodePatch.model_validate(mock_llm_agent("implement add(a, b)", attempt=0))
            except ValidationError as exc:
                validation_feedback = str(exc.errors())
                print("Pydantic caught the LLM hallucination:")
                for error in exc.errors():
                    print(f"- {error['loc']}: {error['msg']}")
                print("Triggering repair loop...\\n")

            print("--- Attempt 2: LLM repairs ---")
            valid_patch = CodePatch.model_validate(mock_llm_agent(validation_feedback, attempt=1))
            print("LLM output validated successfully:")
            print(valid_patch.model_dump_json(indent=2))
            """
        ),
        md(
            """
            ## Framework Mapping

            In production frameworks, you should keep the same mental model: the LLM produces candidate output, and the framework validates it against a schema before another agent or tool consumes it.

            **CrewAI mapping:**

            ```python
            from crewai import Agent, Task, Crew

            coder = Agent(role="Coder", goal="Write code", backstory="...")

            coding_task = Task(
                description="Write the code",
                expected_output="A valid CodePatch",
                agent=coder,
                output_pydantic=CodePatch,  # schema enforcement
            )
            ```

            **LangGraph mapping:**

            ```python
            from typing_extensions import TypedDict

            class AgentState(TypedDict):
                task: TaskSpec
                patch: CodePatch | None
                test_result: TestResult | None
                repair_attempts: int
            ```

            The custom Python version teaches what the framework is doing for you: validate, reject, repair, and only then route forward.
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Hallucination Firewall

            **The Story:** Your Requirements Analyst agent is useful, but it hallucinates. Today it added a `"priority_vibes": "urgent-ish"` field to the handoff. Your Implementation Planner crashes because it expects a typed priority and a bounded risk value. The whole pipeline dies. How do we catch the hallucination before it breaks the system?

            **Your Mission:**
            1. **The Release Truth:** Add a `ReleaseRequest` schema for the software-delivery baseline. It must include `service_name`, `requested_change`, and `priority`.
            2. **The Risk Guardrail:** Add a `ReleasePlan` schema. It must include `deployment_window`, `rollback_plan`, and `risk_level`. Use Pydantic validators to reject high-risk releases with an empty rollback plan.
            3. **The Security Gatekeeper:** Make `ReviewDecision` reject high-risk tasks unless `security_notes` is present and not empty.
            4. **The Gauntlet:** Write one valid and one invalid JSON payload for each schema. Prove that the invalid payloads are caught by `extra="forbid"` or field validators.
            5. **The Feedback Loop:** Convert a `ValidationError` into a structured feedback string that can be fed back into the LLM's prompt for a repair attempt.

            **The Takeaway:** We do not trust the LLM to be perfect. We trust the schema to catch the imperfection. Pydantic is the bouncer at the door of your AI workforce.
            """
        ),
        live_llm_cell(
            "CodePatch",
            "Return a safe CodePatch that implements add(a, b) in math.py with one test named test_add.",
        ),
    ]


def nb5() -> list[dict]:
    return [
        md(
            """
            # NB5: ChatDev-Style Self-Repair Loop

            **2-minute intro script:** Multi-agent systems should not ship the first answer blindly. In ChatDev-style collaboration, a Coder produces work, QA tests it, a Reviewer rejects it with evidence, and the Coder repairs it. The danger is unbounded autonomy: if repair has no retry budget, the system can loop forever. This notebook implements bounded repair with typed patches, typed test results, and repair memory.
            """
        ),
        code(
            """
            from pydantic import BaseModel, ConfigDict, Field, ValidationError
            from typing import List, Optional

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class CodePatch(StrictModel):
                files: dict[str, str]
                rationale: str

            class TestResult(StrictModel):
                passed: bool
                error_log: str | None = None
                failing_tests: List[str] = Field(default_factory=list)

            class RepairMemory(StrictModel):
                original_task: str
                attempt_number: int
                last_error: str | None
                patches_tried: List[str] = Field(default_factory=list)
            """
        ),
        code(
            """
            class BoundedRepairLoop:
                \"\"\"ChatDev-style self-repair with bounded retries.\"\"\"

                def __init__(self, max_repairs: int = 3):
                    self.max_repairs = max_repairs
                    self.memory: Optional[RepairMemory] = None

                def execute_tests(self, patch: CodePatch) -> TestResult:
                    # [DETERMINISTIC MOCK] Replace with a sandboxed test runner
                    # in production. This isolates the repair-loop mechanics.
                    if "buggy" in patch.rationale.lower():
                        return TestResult(
                            passed=False,
                            error_log="AssertionError: expected 2+2=4, got 5",
                            failing_tests=["test_addition"],
                        )
                    return TestResult(passed=True)

                def repair(self, task: str, initial_patch: CodePatch) -> tuple[CodePatch, str]:
                    self.memory = RepairMemory(
                        original_task=task,
                        attempt_number=0,
                        last_error=None,
                        patches_tried=[],
                    )
                    current_patch = initial_patch

                    for attempt in range(self.max_repairs + 1):
                        self.memory.attempt_number = attempt
                        self.memory.patches_tried.append(current_patch.rationale)

                        print(f"\\n=== Attempt {attempt + 1}/{self.max_repairs + 1} ===")
                        print(f"Patch: {current_patch.rationale}")

                        result = self.execute_tests(current_patch)
                        if result.passed:
                            print(f"Tests passed on attempt {attempt + 1}")
                            self.memory.last_error = None
                            return current_patch, f"Success after {attempt + 1} attempts"

                        self.memory.last_error = result.error_log
                        print(f"Tests failed: {result.error_log}")

                        if attempt >= self.max_repairs:
                            print(f"Max repairs ({self.max_repairs}) reached. Escalating.")
                            return current_patch, f"Failed after {self.max_repairs + 1} attempts"

                        print("Generating repair based on error...")
                        current_patch = CodePatch(
                            files={"math.py": "def add(a, b): return a + b"},
                            rationale=f"Fixed: {result.failing_tests[0] if result.failing_tests else 'error'}",
                        )

                    return current_patch, "Unknown error"
            """
        ),
        code(
            """
            def demo_repair_loop():
                loop = BoundedRepairLoop(max_repairs=2)
                initial_patch = CodePatch(
                    files={"math.py": "def add(a, b): return a + b + 1"},
                    rationale="buggy implementation that adds extra 1",
                )
                final_patch, summary = loop.repair("Implement add(a, b) function", initial_patch)

                print("\\n=== Final Result ===")
                print(f"Summary: {summary}")
                print(f"Final patch: {final_patch.rationale}")
                print(f"Repair memory: {loop.memory.model_dump()}")

            demo_repair_loop()
            """
        ),
        md(
            """
            ## Schema-Rejection Feedback Loop

            Pydantic errors are not just exceptions. In production repair loops, they become the exact feedback prompt sent back to the LLM. The agent does not simply "try again"; it receives structured evidence about what broke.
            """
        ),
        code(
            """
            def mock_llm_with_schema_feedback(
                task: str,
                validation_error: str | None,
                attempt: int,
            ) -> dict:
                \"\"\"Simulate an LLM that reads validation feedback before retrying.\"\"\"
                if attempt == 0:
                    # First attempt: LLM hallucinates an extra field.
                    return {
                        "files": {"math.py": "def add(a, b): return a + b + 1"},
                        "rationale": "Initial buggy attempt",
                        "extra_commentary": "LLMs love to add extra fields.",
                    }

                # Subsequent attempts: LLM receives the Pydantic error and adapts.
                if validation_error and "extra_commentary" in validation_error:
                    # It fixed the schema error but kept the logic bug.
                    return {
                        "files": {"math.py": "def add(a, b): return a + b + 1"},
                        "rationale": (
                            "Removed extra fields after seeing schema error: "
                            f"{validation_error[:40]}..."
                        ),
                    }

                # Final successful attempt after QA feedback.
                return {
                    "files": {"math.py": "def add(a, b): return a + b"},
                    "rationale": "Fully repaired after schema and QA feedback.",
                }

            print("--- Attempt 1: LLM hallucinates an extra field ---")
            raw_output_1 = mock_llm_with_schema_feedback("Implement add", None, 0)
            schema_error_msg = None

            try:
                CodePatch.model_validate(raw_output_1)
            except ValidationError as exc:
                schema_error_msg = str(exc)
                print(f"Pydantic blocked it: {exc.errors()[0]['msg']}")
                print("Feeding this exact error string back to the LLM for Attempt 2...\\n")

            print("--- Attempt 2: LLM reads the Pydantic error and fixes the schema ---")
            raw_output_2 = mock_llm_with_schema_feedback("Implement add", schema_error_msg, 1)
            try:
                patch_2 = CodePatch.model_validate(raw_output_2)
                print("Schema accepted. The LLM used validation feedback to fix its JSON.")
                print(f"Rationale: {patch_2.rationale}\\n")
            except ValidationError as exc:
                print(f"Still failing schema: {exc}")
            """
        ),
        md(
            """
            ## Typed Escalation

            When repair fails, production systems should not return a vague string like "failed after 3 attempts." They should emit a typed escalation artifact that a human, manager agent, or ticketing system can parse.
            """
        ),
        code(
            """
            from typing import Literal
            from uuid import uuid4

            class EscalationTicket(StrictModel):
                \"\"\"Typed ticket for human or manager review after bounded repair fails.\"\"\"

                ticket_id: str = Field(default_factory=lambda: f"esc-{uuid4().hex[:6]}")
                original_task: str
                failed_attempts: int
                last_schema_error: str | None = None
                last_qa_error: str | None = None
                reason: Literal["max_repairs_exceeded", "token_budget_exhausted"]

            class BoundedRepairLoopV2:
                def __init__(self, max_repairs: int = 2):
                    self.max_repairs = max_repairs

                def run_with_typed_escalation(self, task: str) -> CodePatch | EscalationTicket:
                    current_error: str | None = None
                    last_schema_error: str | None = None
                    last_qa_error: str | None = None

                    for attempt in range(self.max_repairs + 1):
                        print(f"--- LLM Attempt {attempt + 1} ---")
                        raw_output = mock_llm_with_schema_feedback(task, current_error, attempt)

                        try:
                            patch = CodePatch.model_validate(raw_output)
                            print("Schema valid. Passing to QA...")

                            if "a + b + 1" in patch.files["math.py"]:
                                last_qa_error = "QA Failed: add(2,2) returned 5 instead of 4."
                                current_error = last_qa_error
                                print(f"{current_error} Feeding back to LLM...\\n")

                                if attempt >= self.max_repairs:
                                    break
                                continue

                            print("QA passed. Shipping patch.")
                            return patch

                        except ValidationError as exc:
                            last_schema_error = str(exc)
                            current_error = last_schema_error
                            print(f"Schema rejected: {exc.errors()[0]['msg']}")

                    print("\\nRepair budget exhausted. Generating EscalationTicket...")
                    return EscalationTicket(
                        original_task=task,
                        failed_attempts=self.max_repairs + 1,
                        last_schema_error=last_schema_error,
                        last_qa_error=last_qa_error,
                        reason="max_repairs_exceeded",
                    )

            result = BoundedRepairLoopV2(max_repairs=1).run_with_typed_escalation(
                "Implement add(a,b)"
            )
            print(f"\\n=== Final Output Type: {type(result).__name__} ===")
            print(result.model_dump_json(indent=2))
            assert isinstance(result, EscalationTicket)
            """
        ),
        md(
            """
            ## Token Budget Trap

            Repair loops do not only fail because of `max_repairs`. They also fail because each LLM attempt burns tokens. This bridges NB5 self-repair to NB6 cost-aware routing.
            """
        ),
        code(
            """
            class TokenBudgetTracker(StrictModel):
                total_budget: int
                used: int = 0

                def can_afford_attempt(self, estimated_tokens: int) -> bool:
                    return (self.used + estimated_tokens) <= self.total_budget

            def demo_token_budget_exhaustion():
                budget = TokenBudgetTracker(total_budget=1000)

                for attempt in range(5):
                    estimated_tokens = 400
                    if not budget.can_afford_attempt(estimated_tokens):
                        print(f"Attempt {attempt + 1} blocked: token budget exhausted.")
                        ticket = EscalationTicket(
                            original_task="Implement add",
                            failed_attempts=attempt,
                            reason="token_budget_exhausted",
                        )
                        print(ticket.model_dump_json(indent=2))
                        return ticket

                    budget.used += estimated_tokens
                    remaining = budget.total_budget - budget.used
                    print(f"Attempt {attempt + 1} approved. Budget remaining: {remaining}")

                raise AssertionError("Budget demo should exhaust before five attempts.")

            budget_ticket = demo_token_budget_exhaustion()
            assert budget_ticket.reason == "token_budget_exhausted"
            """
        ),
        live_llm_cell(
            "CodePatch",
            "Return a CodePatch for implementing add(a, b). Include files and rationale only.",
        ),
        md(
            """
            ## 🧪 Exercises: Bounded Autonomy

            **The Story:** Your Coder agent is stuck in an infinite loop. It writes bad code, the QA agent rejects it, the Coder writes the exact same bad code, and your AWS bill hits $10,000 before you can pull the plug. We need bounded autonomy.

            **Your Mission:**
            1. **The Safe Sandbox:** Make `execute_tests` actually execute the code in a restricted namespace (using Python's `exec` with a blank `__builtins__` dict).
            2. **The Compounding Errors:** Add a second failure before success. Observe how the `RepairMemory` accumulates the error logs and passes them to the next attempt.
            3. **The Circuit Breaker:** Force all attempts to fail. Confirm that the system gracefully escalates and returns an `EscalationTicket` instead of looping forever.
            4. **The Quality Gate:** Add `ReviewDecision` as a typed reviewer gate *before* the repair loop starts. If the reviewer rejects the patch outright, it shouldn't even enter the repair loop.
            5. **The Institutional Memory:** Store the repair memory in the shared memory pattern from NB2. This allows other agents (like a Project Manager) to query why a task failed.

            ### Builder Exercise: The Bounded Writer Agent

            **The Analogy:** A writer/editor pair is like a junior engineer and a code reviewer. The reviewer should not just say "bad draft." It should return typed feedback the writer can use on the next attempt.

            **Semantic Building Blocks:**
            - `DraftSpec`: the writer's typed artifact.
            - `EditorFeedback`: the reviewer's typed correction signal.
            - `SharedMemory`: the institutional brain that stores target audience and last feedback.
            - `EscalationTicket`: the typed stop sign when retries run out.

            **Your Mission:**
            1. Store `target_audience="Technical Engineers"` in shared memory before the Writer acts.
            2. Make the Writer produce a `DraftSpec` that reads the audience from memory rather than hardcoding it.
            3. Make the Editor reject the first draft with `missing_elements=["Code examples"]`.
            4. Feed that typed feedback into the second Writer attempt.
            5. Set `max_retries_allowed=2`; force all attempts to fail once and prove the loop returns an `EscalationTicket`.

            **Production Check:** A retry is not "try again." It is "try again with the exact typed evidence of what failed."

            **The Takeaway:** Autonomy without boundaries is just automated chaos. Bounded repair is what makes agents safe for production.
            """
        ),
    ]


def nb6() -> list[dict]:
    return [
        md(
            """
            # NB6: Fugu-Style Dynamic Routing

            **2-minute intro script:** A managed agent team should not send every task to the most expensive model. Fugu-style routing treats orchestration as a model-selection problem. Simple tasks go to fast workers, code-heavy tasks go to code specialists, and high-risk reasoning goes to deeper models. This notebook records the analysis, route decision, estimated cost, and estimated latency so routing becomes observable and governable.
            """
        ),
        code(
            """
            from pydantic import BaseModel, ConfigDict
            from typing import Literal
            from enum import Enum
            from datetime import datetime, timezone

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class ModelClass(str, Enum):
                FAST_CHEAP = "fast-cheap"
                BALANCED = "balanced"
                REASONING = "reasoning"
                CODE_SPECIALIST = "code-spec"

            class TaskComplexity(StrictModel):
                complexity: Literal["simple", "medium", "complex"]
                requires_reasoning: bool
                code_heavy: bool
                risk_level: Literal["low", "medium", "high"]

            class ModelSpec(StrictModel):
                cost_label: str
                cost_usd: float
                latency_label: str
                latency_seconds: float

            class RoutingDecision(StrictModel):
                model: ModelClass
                rationale: str
                estimated_cost: str
                estimated_latency: str
                estimated_cost_usd: float
                estimated_latency_seconds: float

            class RouteTraceRecord(StrictModel):
                task: str
                analysis: TaskComplexity
                decision: RoutingDecision
                timestamp_utc: str
            """
        ),
        code(
            """
            class FuguRouter:
                \"\"\"Sakana Fugu-style dynamic routing.

                This is still a deterministic teaching router. In production,
                `analyze_task` can be replaced with a schema-constrained LLM
                classifier or a learned orchestrator, while `route` remains the
                governance boundary that records cost, latency, and rationale.
                \"\"\"

                MODEL_SPECS = {
                    ModelClass.FAST_CHEAP: ModelSpec(
                        cost_label="$0.01", cost_usd=0.01, latency_label="0.5s", latency_seconds=0.5
                    ),
                    ModelClass.BALANCED: ModelSpec(
                        cost_label="$0.10", cost_usd=0.10, latency_label="2s", latency_seconds=2.0
                    ),
                    ModelClass.REASONING: ModelSpec(
                        cost_label="$0.50", cost_usd=0.50, latency_label="10s", latency_seconds=10.0
                    ),
                    ModelClass.CODE_SPECIALIST: ModelSpec(
                        cost_label="$0.05", cost_usd=0.05, latency_label="1s", latency_seconds=1.0
                    ),
                }

                def __init__(self):
                    self.route_trace: list[RouteTraceRecord] = []

                def analyze_task(self, task: str) -> TaskComplexity:
                    # [DETERMINISTIC MOCK] Replace with a schema-constrained LLM
                    # classifier or learned router in production.
                    task_lower = task.lower()
                    requires_reasoning = any(
                        word in task_lower
                        for word in ["why", "explain", "analyze", "design", "compare", "tradeoff"]
                    )
                    code_heavy = any(
                        word in task_lower
                        for word in ["code", "function", "implement", "debug", "jwt", "api", "refactor"]
                    )

                    if len(task.split()) < 10 and not requires_reasoning and not code_heavy:
                        complexity = "simple"
                    elif len(task.split()) > 18 or "architecture" in task_lower:
                        complexity = "complex"
                    else:
                        complexity = "medium"

                    if any(word in task_lower for word in ["security", "secure", "auth", "jwt", "password", "pii"]):
                        risk_level = "high"
                    elif "test" in task_lower or "demo" in task_lower:
                        risk_level = "low"
                    else:
                        risk_level = "medium"

                    return TaskComplexity(
                        complexity=complexity,
                        requires_reasoning=requires_reasoning,
                        code_heavy=code_heavy,
                        risk_level=risk_level,
                    )

                def route(self, task: str) -> RoutingDecision:
                    analysis = self.analyze_task(task)

                    if analysis.risk_level == "high" or analysis.requires_reasoning:
                        model = ModelClass.REASONING
                        rationale = "Requires reasoning or high risk, use reasoning model"
                    elif analysis.code_heavy:
                        model = ModelClass.CODE_SPECIALIST
                        rationale = "Code-heavy task, use code specialist"
                    elif analysis.complexity == "simple":
                        model = ModelClass.FAST_CHEAP
                        rationale = "Simple task, use fast/cheap model"
                    else:
                        model = ModelClass.BALANCED
                        rationale = "Medium complexity, use balanced model"

                    spec = self.MODEL_SPECS[model]
                    decision = RoutingDecision(
                        model=model,
                        rationale=rationale,
                        estimated_cost=spec.cost_label,
                        estimated_latency=spec.latency_label,
                        estimated_cost_usd=spec.cost_usd,
                        estimated_latency_seconds=spec.latency_seconds,
                    )
                    self.route_trace.append(
                        RouteTraceRecord(
                            task=task,
                            analysis=analysis,
                            decision=decision,
                            timestamp_utc=datetime.now(timezone.utc).isoformat(),
                        )
                    )
                    return decision
            """
        ),
        code(
            """
            def demo_fugu_routing():
                router = FuguRouter()
                tasks = [
                    "What's 2+2?",
                    "Implement a secure JWT authentication system",
                    "Write a function to sort a list",
                    "Explain why microservices architecture is better than monolith",
                    "Debug this race condition in concurrent code",
                    "Create a demo landing page",
                ]

                for task in tasks:
                    analysis = router.analyze_task(task)
                    decision = router.route(task)
                    print(f"Task: {task}")
                    print(f"  Complexity: {analysis.complexity}")
                    print(f"  Code-heavy: {analysis.code_heavy}")
                    print(f"  Requires reasoning: {analysis.requires_reasoning}")
                    print(f"  Risk: {analysis.risk_level}")
                    print(f"  -> Route to: {decision.model.value}")
                    print(f"     Rationale: {decision.rationale}")
                    print(f"     Cost: {decision.estimated_cost}, Latency: {decision.estimated_latency}\\n")

                print(f"Route trace records: {len(router.route_trace)}")
                print(router.route_trace[-1].model_dump_json(indent=2))

            demo_fugu_routing()
            """
        ),
        md(
            """
            ## Cost Optimization Challenge

            Fugu routing is not only an architecture pattern. It is a business control. The next cell runs a batch through dynamic routing, then compares it with the naive strategy of sending every task to the reasoning model.
            """
        ),
        code(
            """
            def build_task_batch() -> list[str]:
                base_tasks = [
                    "What's 2+2?",
                    "Summarize this customer email",
                    "Create a demo landing page",
                    "Write a function to sort a list",
                    "Debug this API timeout",
                    "Implement secure JWT auth",
                    "Explain microservices tradeoffs",
                    "Analyze why checkout conversion dropped",
                    "Design a multi-region architecture for payments",
                    "Refactor this code path for readability",
                ]
                return [base_tasks[i % len(base_tasks)] for i in range(100)]

            def compare_dynamic_vs_static(tasks: list[str]) -> dict:
                router = FuguRouter()
                dynamic_decisions = [router.route(task) for task in tasks]
                dynamic_cost = sum(decision.estimated_cost_usd for decision in dynamic_decisions)

                reasoning_spec = FuguRouter.MODEL_SPECS[ModelClass.REASONING]
                static_cost = len(tasks) * reasoning_spec.cost_usd

                savings = static_cost - dynamic_cost
                savings_percent = (savings / static_cost) * 100 if static_cost else 0.0

                return {
                    "task_count": len(tasks),
                    "dynamic_cost": round(dynamic_cost, 2),
                    "static_reasoning_cost": round(static_cost, 2),
                    "savings": round(savings, 2),
                    "savings_percent": round(savings_percent, 1),
                    "route_counts": {
                        model.value: sum(1 for decision in dynamic_decisions if decision.model == model)
                        for model in ModelClass
                    },
                }

            cost_report = compare_dynamic_vs_static(build_task_batch())
            print(cost_report)
            print(
                f"Dynamic routing saved {cost_report['savings_percent']}% "
                f"(${cost_report['savings']}) compared to static reasoning routing."
            )
            """
        ),
        md(
            """
            ## Optional Live Classifier Swap

            Keep the router offline for the core lab. When learners have API keys, replace only `analyze_task()` with a schema-constrained LLM call that returns `TaskComplexity`. The routing policy, model registry, audit trace, and cost accounting stay deterministic.
            """
        ),
        code(
            """
            USE_LIVE_LLM = False

            if USE_LIVE_LLM:
                # Requires:
                #   pip install openai instructor
                #   export OPENAI_API_KEY="..."
                #
                # Production pattern:
                # 1. Ask the LLM only for TaskComplexity.
                # 2. Validate with Pydantic.
                # 3. Keep route() deterministic and auditable.
                import os
                import instructor
                from openai import OpenAI

                client = instructor.from_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))

                live_analysis = client.chat.completions.create(
                    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                    response_model=TaskComplexity,
                    messages=[
                        {
                            "role": "user",
                            "content": "Classify this task for routing: Implement secure JWT auth",
                        }
                    ],
                )
                print(live_analysis.model_dump_json(indent=2))
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Economics of AI

            **The Story:** You have a $50/day budget for your AI agents. The Marketing agent decides it needs to generate 500 ad variations. It sends all 500 tasks to the `REASONING` model. By 10 AM, your budget is exhausted, and the campaign is dead. How do we route tasks intelligently?

            **Your Mission:**
            1. **The Security Detail:** Add a `SECURITY_SPECIALIST` model class. Update the router to automatically route any task containing PII or security keywords to this specialist, regardless of cost.
            2. **The Hard Cap:** Add a monthly budget counter to the router. If the estimated cost of a route exceeds the remaining budget, reject the route and return a `BudgetExhausted` error.
            3. **The Black Box Recorder:** Ensure every route decision is logged to a `route_trace` list with a UTC timestamp. This is your audit trail for the finance team.
            4. **The Smart Router:** Replace the heuristic keyword analysis with a small, schema-constrained LLM classifier that returns a `TaskComplexity` object.
            5. **The CFO Report:** Run the 100-task cost challenge. Submit your results: "Dynamic routing saved X% ($Y) compared to static reasoning routing."

            **The Takeaway:** Fugu routing is not just an architecture pattern. It is a business control. You cannot manage an AI workforce if you cannot manage its burn rate.
            """
        ),
    ]


def nb7() -> list[dict]:
    return [
        md(
            """
            # NB7: Debugging Broken Agents

            **2-minute intro script:** Learners need to see failures before production. This sandbox intentionally triggers schema drift, tool overreach, unbounded repair risk, and memory leakage. The point is diagnostic muscle: when an agent system behaves strangely, check the handoff schema, the tool policy, the retry budget, and the memory filter first.
            """
        ),
        code(
            """
            from pydantic import BaseModel, ConfigDict, ValidationError

            class StrictPatch(BaseModel):
                model_config = ConfigDict(extra="forbid")
                path: str
                content: str

            try:
                StrictPatch(path="app.py", content="print(1)", secret="leak")
            except ValidationError as exc:
                print("Schema drift blocked:", exc.errors()[0]["type"])
            """
        ),
        code(
            """
            allowed = {"coder": {"read_repo"}, "qa": {"run_tests"}}

            def authorize(role, tool):
                if tool not in allowed.get(role, set()):
                    raise PermissionError(f"{role} cannot use {tool}")

            try:
                authorize("coder", "run_tests")
            except PermissionError as exc:
                print("Tool overreach blocked:", exc)
            """
        ),
        code(
            """
            def unsafe_memory_search(records, query):
                return [r for r in records if query.lower() in r.lower()]

            def safe_memory_search(records, query, requester):
                return [
                    r["text"]
                    for r in records
                    if requester in r["visible_to"] and query.lower() in r["text"].lower()
                ]

            records = [
                {"text": "Public design note", "visible_to": {"coder", "qa"}},
                {"text": "Production DB password: super_secret_123", "visible_to": {"security"}},
            ]

            print("Unsafe search leaks:", unsafe_memory_search([r["text"] for r in records], "password"))
            print("Safe search returns:", safe_memory_search(records, "password", "coder"))
            """
        ),
        code(
            """
            max_repairs = 2
            for attempt in range(max_repairs + 1):
                print("repair attempt", attempt)
            else:
                print("Escalate instead of looping forever")
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Broken-Agent Sandbox

            **The Story:** Your capstone team is almost ready to ship. Then the Coder adds a secret field, the QA agent tries to use a tool it does not own, the memory search leaks a password, and the repair loop keeps retrying. This is not a disaster if the system is observable. It is only a disaster if no one knows where the failure entered the pipeline.

            **Your Mission:**
            1. **Schema Drift Drill:** Add a failing example for invalid enum values and prove Pydantic blocks it before downstream agents consume it.
            2. **Unauthorized Tool Drill:** Add an audit log for denied tool calls. The log must include `role`, `tool`, `allowed=False`, and `reason`.
            3. **Memory Leakage Drill:** Create a memory leakage test that fails with `unsafe_memory_search` and passes with `safe_memory_search`.
            4. **Repair Budget Drill:** Add an `EscalationTicket` schema for exhausted repair loops instead of returning loose strings.
            5. **Capstone Readiness Drill:** Write a debugging checklist for your capstone team: schema, tool, memory, repair, route, API boundary.

            **The Takeaway:** Debugging multi-agent teams is management work. When something fails, inspect the contract, the boundary, the memory filter, and the retry budget before blaming the model.
            """
        ),
    ]


def nb8() -> list[dict]:
    return [
        md(
            """
            # NB8: API Boundaries & Asynchronous Orchestration

            **2-minute intro script:** A production multi-agent team does not live inside `if __name__ == "__main__"`. It receives GitHub webhooks, Slack commands, Jira tickets, and A2A HTTP requests. The API boundary is the governance perimeter: messy external JSON arrives, identity is checked, policy is enforced, and only then does the request become a strict internal task. Because agent workflows may take seconds or minutes, the endpoint returns `202 Accepted` immediately and the pipeline runs in the background.
            """
        ),
        md(
            """
            ## Management Principle

            The API gateway is the customs border for your AI workforce. External systems can ask for work, but they do not get direct access to internal agents, tools, memory, or release actions. Every request must cross identity, policy, and schema checks first.
            """
        ),
        code(
            """
            import asyncio
            from typing import Any, Literal
            from uuid import uuid4

            from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException
            from pydantic import BaseModel, ConfigDict, Field

            from src.enterprise_agent_team import product_manager_parse_issue, run_virtual_software_company

            app = FastAPI(title="Virtual Software Company API")

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            # External world: intentionally small, messy, and untrusted.
            class ExternalIssueRequest(StrictModel):
                github_issue_url: str
                priority: str
                requester_email: str

            # Internal identity: external API keys map into zero-trust identities.
            class AgentIdentity(StrictModel):
                role: Literal["product_manager", "vendor_reporter"]
                trust_tier: Literal["public", "confidential"]

            class TaskStatusResponse(StrictModel):
                task_id: str
                status: Literal["PENDING", "RUNNING", "SHIPPED", "ESCALATED"]
                pull_request_summary: dict[str, Any] | None = None

            # Teaching adapter: production uses Redis, Postgres, or a durable queue.
            task_store: dict[str, dict[str, Any]] = {}

            def get_requester_identity(authorization: str = Header(default="")) -> AgentIdentity:
                \"\"\"Map external API keys to internal zero-trust identities.\"\"\"
                token = authorization.removeprefix("Bearer ").strip()
                if token == "sk-internal-admin":
                    return AgentIdentity(role="product_manager", trust_tier="confidential")
                if token == "sk-external-vendor":
                    return AgentIdentity(role="vendor_reporter", trust_tier="public")
                raise HTTPException(status_code=401, detail="Invalid API key")
            """
        ),
        code(
            """
            async def run_company_async(task_id: str, issue_url: str, identity: AgentIdentity) -> None:
                \"\"\"Long-running multi-agent pipeline triggered by the API boundary.\"\"\"
                task_store[task_id]["status"] = "RUNNING"

                # PM converts external request context into a strict internal TaskSpec.
                task_spec = product_manager_parse_issue(
                    f"Task requested by {identity.role} for {issue_url}"
                )

                # Simulate LLM/tool latency. Production uses queues/workers.
                await asyncio.sleep(0.01)

                final_state = run_virtual_software_company(task_spec.goal)
                review = final_state.review.model_dump(mode="json") if final_state.review else {}
                status = "SHIPPED" if review.get("next_action") == "ship" else "ESCALATED"

                task_store[task_id]["status"] = status
                task_store[task_id]["pull_request_summary"] = {
                    "task": final_state.task.model_dump(mode="json") if final_state.task else None,
                    "route_trace": [route.model_dump(mode="json") for route in final_state.route_trace],
                    "review": review,
                    "repair_attempts": final_state.repair_attempts,
                }

            @app.post("/tasks", response_model=TaskStatusResponse, status_code=202)
            async def ingest_issue(
                request: ExternalIssueRequest,
                background_tasks: BackgroundTasks,
                identity: AgentIdentity = Depends(get_requester_identity),
            ) -> TaskStatusResponse:
                # Governance rule: public vendors cannot create high-risk internal work.
                if identity.trust_tier == "public" and request.priority.lower() == "high":
                    raise HTTPException(
                        status_code=403,
                        detail="Vendors cannot set high priority.",
                    )

                task_id = f"task-{uuid4().hex[:8]}"
                task_store[task_id] = {
                    "task_id": task_id,
                    "status": "PENDING",
                    "pull_request_summary": None,
                }

                background_tasks.add_task(
                    run_company_async,
                    task_id,
                    request.github_issue_url,
                    identity,
                )

                return TaskStatusResponse(task_id=task_id, status="PENDING")

            def read_task_status(task_id: str) -> dict[str, Any]:
                if task_id not in task_store:
                    raise HTTPException(status_code=404, detail="Task not found")
                return task_store[task_id]

            @app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
            async def get_task(task_id: str) -> dict[str, Any]:
                return read_task_status(task_id)

            @app.get("/status/{task_id}", response_model=TaskStatusResponse)
            async def get_status(task_id: str) -> dict[str, Any]:
                # Teaching alias: many systems call this a status endpoint.
                return read_task_status(task_id)
            """
        ),
        code(
            """
            from fastapi.testclient import TestClient

            client = TestClient(app)

            print("--- Test 1: Internal admin triggers high-priority task ---")
            response = client.post(
                "/tasks",
                json={
                    "github_issue_url": "https://github.com/org/repo/issues/42",
                    "priority": "high",
                    "requester_email": "pm@company.com",
                },
                headers={"Authorization": "Bearer sk-internal-admin"},
            )
            print(f"Status: {response.status_code} (should be 202)")
            task_id = response.json()["task_id"]
            assert response.status_code == 202

            print("\\n--- Test 2: Poll status endpoint ---")
            status_response = client.get(f"/tasks/{task_id}")
            print(status_response.json())
            assert status_response.status_code == 200
            assert status_response.json()["status"] in {"PENDING", "RUNNING", "SHIPPED", "ESCALATED"}

            print("\\n--- Test 3: External vendor blocked from high priority ---")
            blocked_response = client.post(
                "/tasks",
                json={
                    "github_issue_url": "https://github.com/external/repo/issues/7",
                    "priority": "high",
                    "requester_email": "vendor@external.com",
                },
                headers={"Authorization": "Bearer sk-external-vendor"},
            )
            print(f"Status: {blocked_response.status_code} (should be 403)")
            print(f"Reason: {blocked_response.json()['detail']}")
            assert blocked_response.status_code == 403

            print("\\n--- Test 4: Invalid API key blocked ---")
            bad_key_response = client.post(
                "/tasks",
                json={
                    "github_issue_url": "https://github.com/org/repo/issues/1",
                    "priority": "low",
                    "requester_email": "unknown@example.com",
                },
                headers={"Authorization": "Bearer bad-key"},
            )
            print(f"Status: {bad_key_response.status_code} (should be 401)")
            assert bad_key_response.status_code == 401
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Front Door

            **The Story:** Your multi-agent system is working perfectly in your Jupyter Notebook. But now, the VP of Engineering wants to trigger it from a Slack command, and the Product team wants to trigger it from a GitHub webhook. And they want it to scale to 1,000 concurrent requests.

            **Your Mission:**
            1. **The GitHub Bridge:** Add a `/webhooks/github` alias endpoint. It must parse the raw GitHub JSON payload and map it into the same internal `TaskStatusResponse`.
            2. **The Legacy Client:** Add an `X-API-Key` header variant as an alternative to `Authorization: Bearer`. Many internal tools still use legacy auth headers.
            3. **The Audit Trail:** Store `created_by`, `priority`, and `requester_email` in the `task_store`. When the task completes, include these in the final `PullRequestSummary`.
            4. **The Perimeter Check:** Add a denied-memory-access test. Prove that a `vendor_reporter` identity cannot query the shared memory for internal tasks.
            5. **The Production Reality:** Replace the in-memory `task_store` dictionary with a design note for Redis or PostgreSQL. How would you handle concurrent writes to the same `task_id`?

            **The Takeaway:** The API gateway is the customs border for your AI workforce. External systems can ask for work, but they do not get direct access to your agents.
            """
        ),
    ]


def nb9() -> list[dict]:
    return [
        md(
            """
            # NB9: Advanced Fugu Orchestration

            NB6 teaches the first rung: rule-based heterogeneous routing. Sakana Fugu goes further. It studies learned orchestrator models, dynamic workflow scaffolds, collective intelligence, isolation between workflows, persistent memory, and adaptive topology selection. This notebook bridges that gap with offline teaching adapters: a scaffold generator, a debate moderator, a workflow restructurer, and a simple learner that updates routing rules from history.
            """
        ),
        md(
            """
            ## 1. The Limitation of Rule-Based Routing

            A keyword router can be useful, but it is not learned orchestration. It can choose a model class, but it does not invent a workflow, aggregate disagreement, or adapt after repeated failures. The production mindset is: routing is one decision inside orchestration, not the whole system.
            """
        ),
        code(
            """
            from collections import defaultdict
            from enum import Enum
            from typing import Literal

            from pydantic import BaseModel, ConfigDict, Field

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class ModelClass(str, Enum):
                FAST_CHEAP = "fast-cheap"
                BALANCED = "balanced"
                REASONING = "reasoning"
                CODE_SPECIALIST = "code-specialist"

            class AgentRole(str, Enum):
                PRODUCT_MANAGER = "product_manager"
                CODER = "coder"
                QA = "qa"
                SECURITY_REVIEWER = "security_reviewer"
                COMPLIANCE_AGENT = "compliance_agent"
                REVIEWER = "reviewer"
                HUMAN = "human"

            class TaskComplexity(StrictModel):
                complexity: Literal["simple", "medium", "complex"]
                requires_reasoning: bool
                code_heavy: bool
                risk_level: Literal["low", "medium", "high"]
                word_count: int

            class WorkflowScaffold(StrictModel):
                agents_needed: list[AgentRole]
                execution_order: list[tuple[AgentRole, AgentRole]]
                parallel_groups: list[list[AgentRole]] = Field(default_factory=list)
                estimated_total_cost: float
                estimated_total_latency: float

            class DebateRecord(StrictModel):
                topic: str
                agent_a_position: str
                agent_b_position: str
                points_of_agreement: list[str]
                points_of_contention: list[str]
                final_decision: str
                escalation_required: bool = False

            class EscalationTicket(StrictModel):
                reason: str
                source: Literal["debate", "repair_budget", "human_review"]
                evidence: list[str] = Field(default_factory=list)

            class RoutingHistory(StrictModel):
                task_description: str
                task_features: dict[str, float]
                chosen_model: ModelClass
                actual_cost_usd: float
                actual_latency_seconds: float
                success_score: float = Field(ge=0.0, le=1.0)
            """
        ),
        md(
            """
            ## 2. Dynamic Scaffold Generation

            Fugu-style orchestration asks a larger question than "which model should answer?" It asks, "what workflow should exist for this task?" A simple task may need one analyst. A security audit needs a reviewer and a compliance agent. The scaffold is created from the task, not hard-coded into the application.
            """
        ),
        code(
            """
            class ScaffoldGenerator:
                def analyze_task(self, task: str) -> TaskComplexity:
                    text = task.lower()
                    words = text.split()
                    high_risk_terms = {"security", "audit", "auth", "compliance", "payment", "pii"}
                    code_terms = {"implement", "code", "api", "function", "test"}
                    reasoning_terms = {"design", "strategy", "architecture", "tradeoff", "audit"}

                    risk_level = "high" if any(term in text for term in high_risk_terms) else "medium"
                    if len(words) <= 4 and risk_level != "high":
                        complexity = "simple"
                    elif len(words) <= 10 and "strategy" not in text and risk_level != "high":
                        complexity = "medium"
                    else:
                        complexity = "complex"

                    return TaskComplexity(
                        complexity=complexity,
                        requires_reasoning=any(term in text for term in reasoning_terms) or risk_level == "high",
                        code_heavy=any(term in text for term in code_terms),
                        risk_level=risk_level,
                        word_count=len(words),
                    )

                def generate(self, task: str, complexity: TaskComplexity) -> WorkflowScaffold:
                    text = task.lower()

                    if "security" in text or "audit" in text or "compliance" in text:
                        return WorkflowScaffold(
                            agents_needed=[
                                AgentRole.PRODUCT_MANAGER,
                                AgentRole.SECURITY_REVIEWER,
                                AgentRole.COMPLIANCE_AGENT,
                                AgentRole.REVIEWER,
                            ],
                            execution_order=[
                                (AgentRole.PRODUCT_MANAGER, AgentRole.SECURITY_REVIEWER),
                                (AgentRole.PRODUCT_MANAGER, AgentRole.COMPLIANCE_AGENT),
                                (AgentRole.SECURITY_REVIEWER, AgentRole.REVIEWER),
                                (AgentRole.COMPLIANCE_AGENT, AgentRole.REVIEWER),
                            ],
                            parallel_groups=[[AgentRole.SECURITY_REVIEWER, AgentRole.COMPLIANCE_AGENT]],
                            estimated_total_cost=0.42,
                            estimated_total_latency=8.0,
                        )

                    if complexity.complexity == "simple":
                        return WorkflowScaffold(
                            agents_needed=[AgentRole.PRODUCT_MANAGER],
                            execution_order=[],
                            parallel_groups=[],
                            estimated_total_cost=0.01,
                            estimated_total_latency=0.5,
                        )

                    if complexity.complexity == "medium":
                        return WorkflowScaffold(
                            agents_needed=[AgentRole.PRODUCT_MANAGER, AgentRole.CODER],
                            execution_order=[(AgentRole.PRODUCT_MANAGER, AgentRole.CODER)],
                            parallel_groups=[],
                            estimated_total_cost=0.08,
                            estimated_total_latency=2.0,
                        )

                    return WorkflowScaffold(
                        agents_needed=[
                            AgentRole.PRODUCT_MANAGER,
                            AgentRole.CODER,
                            AgentRole.QA,
                            AgentRole.REVIEWER,
                        ],
                        execution_order=[
                            (AgentRole.PRODUCT_MANAGER, AgentRole.CODER),
                            (AgentRole.PRODUCT_MANAGER, AgentRole.QA),
                            (AgentRole.CODER, AgentRole.REVIEWER),
                            (AgentRole.QA, AgentRole.REVIEWER),
                        ],
                        parallel_groups=[[AgentRole.CODER, AgentRole.QA]],
                        estimated_total_cost=0.22,
                        estimated_total_latency=5.0,
                    )

            generator = ScaffoldGenerator()
            tasks = [
                "Classify ticket",
                "Draft release plan",
                "Run security audit for auth workflow",
            ]

            for task in tasks:
                complexity = generator.analyze_task(task)
                scaffold = generator.generate(task, complexity)
                print(f"Task: {task}")
                print(f"Complexity: {complexity.complexity}, risk={complexity.risk_level}")
                print(f"Agents: {[agent.value for agent in scaffold.agents_needed]}")
                print(f"Parallel: {[[agent.value for agent in group] for group in scaffold.parallel_groups]}")
                print()

            security_scaffold = generator.generate(
                "security audit",
                generator.analyze_task("security audit"),
            )
            assert AgentRole.SECURITY_REVIEWER in security_scaffold.agents_needed
            assert AgentRole.COMPLIANCE_AGENT in security_scaffold.agents_needed
            """
        ),
        md(
            """
            ## 3. Collective Intelligence via Debate

            For complex decisions, one agent's answer is often not enough. A debate pattern asks multiple agents for positions, extracts agreement and contention, and either synthesizes a decision or escalates. This is not free-form argument; it is structured disagreement with a typed record.
            """
        ),
        code(
            """
            class DebateModerator:
                STOPWORDS = {
                    "the", "a", "an", "for", "and", "or", "to", "use", "with",
                    "data", "system", "because", "when", "is", "are",
                }

                def _keywords(self, text: str) -> set[str]:
                    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
                    return {
                        word
                        for word in cleaned.split()
                        if len(word) > 2 and word not in self.STOPWORDS
                    }

                def moderate(self, topic: str, position_a: str, position_b: str) -> DebateRecord:
                    keywords_a = self._keywords(position_a)
                    keywords_b = self._keywords(position_b)
                    agreements = sorted(keywords_a & keywords_b)
                    contentions = sorted((keywords_a ^ keywords_b))[:8]

                    combined = f"{position_a} {position_b}".lower()
                    if "postgresql" in combined and ("mongodb" in combined or "nosql" in combined):
                        final = "Use PostgreSQL for relational data and Redis for caching."
                        escalation = False
                    elif not agreements and len(contentions) > 6:
                        final = "Escalate to a human architect; the agents disagree without enough overlap."
                        escalation = True
                    else:
                        final = "Adopt the shared requirements and run a small validation experiment."
                        escalation = False

                    return DebateRecord(
                        topic=topic,
                        agent_a_position=position_a,
                        agent_b_position=position_b,
                        points_of_agreement=agreements,
                        points_of_contention=contentions,
                        final_decision=final,
                        escalation_required=escalation,
                    )

            moderator = DebateModerator()
            debate = moderator.moderate(
                topic="PostgreSQL vs MongoDB for customer platform",
                position_a="Use PostgreSQL because customer orders need relational consistency.",
                position_b="Use MongoDB or NoSQL for flexible profiles, but add Redis for fast caching.",
            )
            print(debate.model_dump_json(indent=2))
            assert debate.final_decision == "Use PostgreSQL for relational data and Redis for caching."

            unresolved_debate = moderator.moderate(
                topic="Release readiness",
                position_a="Coder says ship now because tests passed.",
                position_b="Security reviewer says block release because auth token handling is incomplete.",
            )
            if unresolved_debate.escalation_required:
                ticket = EscalationTicket(
                    reason="Debate moderator could not resolve release readiness.",
                    source="debate",
                    evidence=unresolved_debate.points_of_contention,
                )
                print(ticket.model_dump_json(indent=2))
            """
        ),
        md(
            """
            ## 4. Adaptive Topology Selection

            Static pipelines hide failure. Adaptive orchestration changes the workflow when evidence says the current topology is wrong. If QA fails because security was missing, add Security and Compliance in parallel before the final reviewer.
            """
        ),
        code(
            """
            class WorkflowRestructurer:
                def restructure(self, scaffold: WorkflowScaffold, failure_reason: str) -> WorkflowScaffold:
                    text = failure_reason.lower()
                    agents = list(scaffold.agents_needed)
                    edges = list(scaffold.execution_order)
                    parallel_groups = [list(group) for group in scaffold.parallel_groups]

                    if "security" in text or "compliance" in text:
                        for agent in [AgentRole.SECURITY_REVIEWER, AgentRole.COMPLIANCE_AGENT]:
                            if agent not in agents:
                                agents.append(agent)
                        if AgentRole.REVIEWER not in agents:
                            agents.append(AgentRole.REVIEWER)
                        edges.extend([
                            (AgentRole.SECURITY_REVIEWER, AgentRole.REVIEWER),
                            (AgentRole.COMPLIANCE_AGENT, AgentRole.REVIEWER),
                        ])
                        parallel_groups.append([AgentRole.SECURITY_REVIEWER, AgentRole.COMPLIANCE_AGENT])

                    return WorkflowScaffold(
                        agents_needed=agents,
                        execution_order=edges,
                        parallel_groups=parallel_groups,
                        estimated_total_cost=round(scaffold.estimated_total_cost + 0.18, 2),
                        estimated_total_latency=round(scaffold.estimated_total_latency + 3.0, 2),
                    )

            initial = generator.generate(
                "Draft API implementation plan",
                generator.analyze_task("Draft API implementation plan"),
            )
            restructured = WorkflowRestructurer().restructure(
                initial,
                "QA failed because security and compliance review were missing.",
            )
            print("Before:", [agent.value for agent in initial.agents_needed])
            print("After:", [agent.value for agent in restructured.agents_needed])
            assert AgentRole.SECURITY_REVIEWER in restructured.agents_needed
            assert AgentRole.COMPLIANCE_AGENT in restructured.agents_needed
            """
        ),
        md(
            """
            ## 5. From Heuristics to Learning

            A production orchestrator should learn from history. This simple learner is intentionally small: it looks at the last ten routing decisions, identifies repeated low-success choices, and updates the routing table. It is not the full Sakana Fugu method, but it shows the bridge from static rules to learned orchestration.
            """
        ),
        code(
            """
            class SimpleLearner:
                def __init__(self):
                    self.learned_rules: dict[str, ModelClass] = {}

                def extract_features(self, task: str) -> dict[str, float]:
                    text = task.lower()
                    return {
                        "has_security": 1.0 if "security" in text or "audit" in text else 0.0,
                        "has_strategy": 1.0 if "strategy" in text or "design" in text else 0.0,
                        "has_bulk": 1.0 if "500" in text or "variations" in text else 0.0,
                        "word_count": float(len(text.split())),
                    }

                def route(self, task: str) -> ModelClass:
                    features = self.extract_features(task)
                    for feature, model in self.learned_rules.items():
                        if features.get(feature, 0.0) > 0.0:
                            return model
                    if features["has_bulk"]:
                        return ModelClass.FAST_CHEAP
                    if features["has_strategy"]:
                        return ModelClass.REASONING
                    return ModelClass.FAST_CHEAP

                def analyze_history(self, history: list[RoutingHistory]) -> dict[ModelClass, list[str]]:
                    buckets: dict[ModelClass, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
                    for item in history[-10:]:
                        for feature, value in item.task_features.items():
                            if value > 0.0 and feature != "word_count":
                                buckets[item.chosen_model][feature].append(item.success_score)

                    patterns: dict[ModelClass, list[str]] = {}
                    for model, feature_scores in buckets.items():
                        strong_features = []
                        for feature, scores in feature_scores.items():
                            avg_score = sum(scores) / len(scores)
                            if avg_score >= 0.8:
                                strong_features.append(feature)
                        patterns[model] = strong_features
                    return patterns

                def update_rules(self, history: list[RoutingHistory]) -> None:
                    recent = history[-10:]
                    failure_counts: dict[str, int] = defaultdict(int)

                    for item in recent:
                        for feature, value in item.task_features.items():
                            if value <= 0.0 or feature == "word_count":
                                continue
                            if item.success_score < 0.5:
                                failure_counts[feature] += 1

                    for feature, count in failure_counts.items():
                        if count >= 5 and feature in {"has_security", "has_strategy"}:
                            self.learned_rules[feature] = ModelClass.REASONING
                        elif count >= 5 and feature == "has_bulk":
                            self.learned_rules[feature] = ModelClass.BALANCED

            learner = SimpleLearner()
            task = "security audit for login workflow"
            print("Before learning:", learner.route(task).value)

            failed_history = [
                RoutingHistory(
                    task_description=f"security audit attempt {i}",
                    task_features=learner.extract_features(task),
                    chosen_model=ModelClass.FAST_CHEAP,
                    actual_cost_usd=0.01,
                    actual_latency_seconds=0.5,
                    success_score=0.2,
                )
                for i in range(10)
            ]

            learner.update_rules(failed_history)
            print("Learned rules:", {k: v.value for k, v in learner.learned_rules.items()})
            print("After learning:", learner.route(task).value)
            assert learner.route(task) == ModelClass.REASONING
            """
        ),
        md(
            """
            ## 6. Intelligent Orchestrator Pattern

            The next step beyond deterministic routing is an LLM manager that reads team state and chooses a typed action. The LLM does not execute arbitrary code. It emits a `DelegationDecision`; the framework validates that decision, then calls approved tools such as `delegate_to_coder`, `delegate_to_qa`, or `escalate_to_human`.
            """
        ),
        code(
            """
            class TaskSpec(StrictModel):
                goal: str
                acceptance_criteria: list[str]
                risk_level: Literal["low", "medium", "high"] = "medium"

            class CodePatch(StrictModel):
                files: dict[str, str]
                rationale: str

            class TeamStateSnapshot(StrictModel):
                task: TaskSpec
                patch: CodePatch | None = None
                repair_attempts: int = 0
                max_repairs: int = 2
                last_error: str | None = None

            class DelegationDecision(StrictModel):
                action: Literal["delegate", "escalate", "review"]
                target_agent: AgentRole
                payload: dict
                rationale: str

            def delegate_to_coder(task: TaskSpec) -> CodePatch:
                return CodePatch(
                    files={"app.py": "def add(a, b): return a + b"},
                    rationale=f"Coder implemented task: {task.goal}",
                )

            def delegate_to_qa(patch: CodePatch) -> dict:
                passed = "return a + b" in patch.files.get("app.py", "")
                return {"passed": passed, "log": "QA passed" if passed else "QA failed"}

            def escalate_to_human(reason: str) -> dict:
                return {"status": "ESCALATED_TO_HUMAN", "reason": reason}

            def mock_llm_orchestrator(state: TeamStateSnapshot) -> dict:
                \"\"\"Teaching adapter for an LLM manager with tool-calling intent.\"\"\"
                if state.repair_attempts >= state.max_repairs:
                    return {
                        "action": "escalate",
                        "target_agent": AgentRole.HUMAN,
                        "payload": {
                            "reason": f"Repair budget exhausted after {state.repair_attempts} attempts."
                        },
                        "rationale": "The workflow should stop and request human review.",
                    }
                if state.patch is None:
                    return {
                        "action": "delegate",
                        "target_agent": AgentRole.CODER,
                        "payload": {"task": state.task.model_dump(mode="json")},
                        "rationale": "No patch exists yet, so delegate implementation to coder.",
                    }
                return {
                    "action": "review",
                    "target_agent": AgentRole.QA,
                    "payload": {"patch": state.patch.model_dump(mode="json")},
                    "rationale": "A patch exists and must be tested before release.",
                }

            def execute_delegation(decision: DelegationDecision) -> dict:
                if decision.action == "delegate" and decision.target_agent == AgentRole.CODER:
                    task = TaskSpec.model_validate(decision.payload["task"])
                    return {"patch": delegate_to_coder(task).model_dump(mode="json")}
                if decision.action == "review" and decision.target_agent == AgentRole.QA:
                    patch = CodePatch.model_validate(decision.payload["patch"])
                    return {"qa": delegate_to_qa(patch)}
                if decision.action == "escalate" and decision.target_agent == AgentRole.HUMAN:
                    return escalate_to_human(str(decision.payload["reason"]))
                raise ValueError(f"Unsupported delegation decision: {decision}")

            active_state = TeamStateSnapshot(
                task=TaskSpec(
                    goal="Implement add endpoint",
                    acceptance_criteria=["Return correct sums", "Include tests"],
                )
            )
            decision = DelegationDecision.model_validate(mock_llm_orchestrator(active_state))
            print(decision.model_dump_json(indent=2))
            coder_result = execute_delegation(decision)
            assert "patch" in coder_result

            exhausted_state = TeamStateSnapshot(
                task=active_state.task,
                repair_attempts=2,
                max_repairs=2,
                last_error="QA failed twice",
            )
            escalation_decision = DelegationDecision.model_validate(
                mock_llm_orchestrator(exhausted_state)
            )
            escalation_result = execute_delegation(escalation_decision)
            print(escalation_result)
            assert escalation_decision.action == "escalate"
            assert escalation_result["status"] == "ESCALATED_TO_HUMAN"
            """
        ),
        md(
            """
            ## 🧪 Exercises: The Internal Brain

            **The Story:** Your first agent chain worked when every task was simple. Then the CEO asked for a secure login system, the Coder wanted to ship, the Security Reviewer wanted to block, and the old linear pipeline had no place to resolve the conflict. A real manager brain must decide the workflow shape, organize disagreement, and know when to escalate.

            **Your Mission:** Agents must do more than pass notes. They must scaffold workflows, debate conflicting evidence, and route based on complexity.

            ### Exercise 9.1: The Dynamic Scaffold

            **Problem:** A linear chain fails when the task is complex. A simple task may need one agent; a high-risk task may need Product Manager → Coder → Security Reviewer → QA → Reviewer.

            **Task:** Implement or extend `WorkflowScaffold`.

            **Input:** `TaskComplexity` from NB6-style routing.

            **Output:** `agents_needed`, `execution_order`, and `parallel_groups`.

            **The Nail:** If `risk_level == "high"`, the scaffold must automatically insert `SecurityReviewer` before `Reviewer`.

            ### Exercise 9.2: The Debate Protocol

            **Problem:** The Coder says "ship"; the Security Reviewer says "block." Who wins?

            **Task:** Implement or extend `DebateRecord` and `DebateModerator`.

            **Required fields:** `agent_a_position`, `agent_b_position`, `points_of_contention`, `final_decision`, and `escalation_required`.

            **The Nail:** If the Moderator cannot resolve the contention, it must emit an `EscalationTicket` for the human steering layer in NB10.

            ### Bridge to NB10

            NB9 is the Internal Brain. It builds the workflow and manages disagreement. NB10 is the External Steering Wheel. When NB9 cannot resolve contention, NB10 lets the human update TeamLog or veto the release.

            **The Takeaway:** Advanced orchestration is not "more agents." It is the management layer that decides which agents are needed, how they connect, how disagreement is resolved, and when a human must step in.
            """
        ),
    ]


def nb10() -> list[dict]:
    return [
        md(
            """
            # NB10: Vibe Coding CEO Interface

            Vibe coding is not "let the model do whatever it wants." In this course, vibe coding means a human acts as CEO of an AI workforce: describing intent in natural language, reviewing typed plans, changing direction mid-workflow, and approving or rejecting the final pull request summary.
            """
        ),
        md(
            """
            ## Management Principle

            The human does not micromanage every token. The human manages goals, constraints, and approvals. The system converts conversational instructions into typed artifacts that agents can safely execute.
            """
        ),
        code(
            """
            from enum import Enum
            from typing import Literal
            from uuid import uuid4

            from pydantic import BaseModel, ConfigDict, Field

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class AgentRole(str, Enum):
                CEO = "ceo"
                MANAGER = "manager"
                CODER = "coder"
                QA = "qa"
                SECURITY = "security"
                RELEASE = "release"

            class ManagerInstruction(StrictModel):
                raw_text: str
                intent: Literal["create_project", "modify_constraint", "approve", "reject"]
                requested_by: AgentRole = AgentRole.CEO

            class ProjectPlan(StrictModel):
                project_id: str = Field(default_factory=lambda: f"proj-{uuid4().hex[:6]}")
                goal: str
                api_style: Literal["REST", "GraphQL"] = "REST"
                database_choice: Literal["PostgreSQL", "MongoDB", "SQLite"]
                acceptance_criteria: list[str] = Field(min_length=1)
                risk_level: Literal["low", "medium", "high"]

            class TeamCommitment(StrictModel):
                commitment_id: str = Field(default_factory=lambda: f"commit-{uuid4().hex[:6]}")
                owner: AgentRole
                key: str
                value: str
                reason: str

            class HumanReviewDecision(StrictModel):
                status: Literal["approved", "rejected", "needs_changes"]
                reviewer: str
                notes: str

            class CodePatch(StrictModel):
                files: dict[str, str]
                rationale: str

            class TestResult(StrictModel):
                passed: bool
                log: str

            class SecurityReview(StrictModel):
                approved: bool
                findings: list[str] = Field(default_factory=list)

            class PullRequestSummary(StrictModel):
                title: str
                body: str
                database_choice: str
                approved_by_human: bool
                audit_trail: list[str]

            class SharedMemory:
                def __init__(self):
                    self.commitments: list[TeamCommitment] = []

                def add_commitment(self, commitment: TeamCommitment) -> None:
                    self.commitments.append(commitment)

                def latest(self, key: str) -> TeamCommitment | None:
                    matches = [item for item in self.commitments if item.key == key]
                    return matches[-1] if matches else None
            """
        ),
        code(
            """
            def parse_manager_instruction(text: str) -> ManagerInstruction:
                lowered = text.lower()
                if "actually" in lowered or "instead" in lowered or "change" in lowered:
                    intent = "modify_constraint"
                elif "approve" in lowered:
                    intent = "approve"
                elif "reject" in lowered:
                    intent = "reject"
                else:
                    intent = "create_project"
                return ManagerInstruction(raw_text=text, intent=intent)

            def mock_manager_llm_extract_plan(text: str) -> dict:
                \"\"\"Teaching adapter: simulates an LLM translating natural language into a ProjectPlan candidate.\"\"\"
                lowered = text.lower()
                if "database that doesn't exist" in lowered:
                    database = "ImaginaryDB"  # Pydantic must reject this.
                elif "mongodb" in lowered:
                    database = "MongoDB"
                elif "postgres" in lowered or "postgresql" in lowered:
                    database = "PostgreSQL"
                else:
                    database = "SQLite"

                return {
                    "goal": text,
                    "api_style": "GraphQL" if "graphql" in lowered else "REST",
                    "database_choice": database,
                    "acceptance_criteria": [
                        "Expose user registration endpoint",
                        "Expose login endpoint",
                        "Persist users in the selected database",
                        "Include tests and security review",
                    ],
                    "risk_level": "high" if "auth" in lowered or "secure" in lowered else "medium",
                }

            def manager_create_plan(instruction: ManagerInstruction) -> ProjectPlan:
                return ProjectPlan.model_validate(
                    mock_manager_llm_extract_plan(instruction.raw_text)
                )

            def manager_apply_human_change(
                plan: ProjectPlan,
                instruction: ManagerInstruction,
                memory: SharedMemory,
            ) -> ProjectPlan:
                text = instruction.raw_text.lower()
                update = {}
                if "mongodb" in text:
                    update["database_choice"] = "MongoDB"
                    memory.add_commitment(
                        TeamCommitment(
                            owner=AgentRole.CEO,
                            key="db",
                            value="MongoDB",
                            reason="Human CEO changed persistence requirement mid-workflow.",
                        )
                    )
                elif "postgres" in text:
                    update["database_choice"] = "PostgreSQL"
                    memory.add_commitment(
                        TeamCommitment(
                            owner=AgentRole.CEO,
                            key="db",
                            value="PostgreSQL",
                            reason="Human CEO restored relational persistence requirement.",
                        )
                    )
                return plan.model_copy(update=update)
            """
        ),
        code(
            """
            def coder_agent(plan: ProjectPlan, memory: SharedMemory) -> CodePatch:
                db_commitment = memory.latest("db")
                database = db_commitment.value if db_commitment else plan.database_choice
                return CodePatch(
                    files={
                        "auth_api.py": (
                            f"DATABASE = '{database}'\\n"
                            "def register_user(email, password):\\n"
                            "    return {'status': 'created', 'email': email}\\n"
                            "def login(email, password):\\n"
                            "    return {'token': 'mock-jwt'}\\n"
                        )
                    },
                    rationale=f"Implemented {plan.api_style} auth API using {database}.",
                )

            def qa_agent(patch: CodePatch) -> TestResult:
                content = patch.files["auth_api.py"]
                required = ["register_user", "login", "DATABASE"]
                missing = [name for name in required if name not in content]
                return TestResult(
                    passed=not missing,
                    log="All auth API checks passed" if not missing else f"Missing: {missing}",
                )

            def security_agent(plan: ProjectPlan, patch: CodePatch) -> SecurityReview:
                findings = []
                content = patch.files["auth_api.py"]
                if "password" not in content:
                    findings.append("Authentication flow does not mention password handling.")
                if plan.risk_level == "high" and "mock-jwt" in content:
                    findings.append("Teaching mock JWT must be replaced before production.")
                return SecurityReview(approved=True, findings=findings)

            def release_manager(
                plan: ProjectPlan,
                patch: CodePatch,
                tests: TestResult,
                security: SecurityReview,
                human_decision: HumanReviewDecision,
                audit_trail: list[str],
            ) -> PullRequestSummary:
                return PullRequestSummary(
                    title="Build user authentication API",
                    body=(
                        f"Goal: {plan.goal}\\n"
                        f"Database: {plan.database_choice}\\n"
                        f"Patch rationale: {patch.rationale}\\n"
                        f"QA: {tests.log}\\n"
                        f"Security findings: {security.findings}"
                    ),
                    database_choice=plan.database_choice,
                    approved_by_human=human_decision.status == "approved",
                    audit_trail=audit_trail,
                )
            """
        ),
        code(
            """
            def run_vibe_coding_session(scripted_inputs: list[str]) -> PullRequestSummary:
                memory = SharedMemory()
                audit_trail: list[str] = []

                create_instruction = parse_manager_instruction(scripted_inputs[0])
                plan = manager_create_plan(create_instruction)
                memory.add_commitment(
                        TeamCommitment(
                            owner=AgentRole.MANAGER,
                            key="db",
                            value=plan.database_choice,
                            reason="Initial project plan from CEO instruction.",
                        )
                    )
                audit_trail.append(f"CEO request parsed into ProjectPlan using {plan.database_choice}")

                change_instruction = parse_manager_instruction(scripted_inputs[1])
                plan = manager_apply_human_change(plan, change_instruction, memory)
                audit_trail.append(f"CEO modified database choice to {plan.database_choice}")

                patch = coder_agent(plan, memory)
                tests = qa_agent(patch)
                security = security_agent(plan, patch)
                audit_trail.append(f"Coder produced patch: {patch.rationale}")
                audit_trail.append(f"QA result: {tests.log}")
                audit_trail.append(f"Security approved with findings: {security.findings}")

                human_decision = HumanReviewDecision(
                    status="approved",
                    reviewer="human-ceo",
                    notes="Approved after confirming MongoDB requirement was honored.",
                )
                audit_trail.append(f"Human review status={human_decision.status}")

                return release_manager(
                    plan=plan,
                    patch=patch,
                    tests=tests,
                    security=security,
                    human_decision=human_decision,
                    audit_trail=audit_trail,
                )

            summary = run_vibe_coding_session([
                "Build a REST API for user authentication with PostgreSQL",
                "Actually, use MongoDB instead",
            ])
            print(summary.model_dump_json(indent=2))

            assert summary.database_choice == "MongoDB"
            assert summary.approved_by_human is True
            assert any("modified database choice to MongoDB" in event for event in summary.audit_trail)

            try:
                manager_create_plan(parse_manager_instruction("Build a REST API. Use a database that doesn't exist."))
                raise AssertionError("Invalid database should not validate.")
            except Exception as exc:
                print(f"Validation blocked invalid CEO instruction: {type(exc).__name__}")
            """
        ),
        md(
            """
            ## CLI or Gradio Upgrade

            The previous cell uses scripted inputs so the notebook is testable offline. To turn it into a real interface, wrap `run_vibe_coding_session` with either:

            - a CLI loop that calls `input()` for each CEO instruction, or
            - a Gradio text box that appends each instruction to session state.

            Keep the same typed schemas. The interface changes, but the management contracts stay stable.
            """
        ),
        md(
            """
            ## 🧪 Exercises: The CEO's Steering Wheel

            **The Story:** The CEO does not open `ProjectPlan` and edit JSON. The CEO says, "Build secure login," then later says, "Actually, use MongoDB and fix the security flaw." If that raw text flows straight to the Coder, the system becomes prompt soup. The manager must translate human intent into durable TeamLog state.

            **Your Mission:** The CEO does not write Pydantic schemas. The CEO writes, "Make it faster and use MongoDB." The system must translate that chaos into governed state.

            ### Exercise 10.1: The Translation Layer

            **Problem:** The CEO says, "Build a REST API for auth." The Coder needs a strict `ProjectPlan`.

            **Task:** Write or extend `parse_manager_instruction()` and `manager_create_plan()`.

            **Constraint:** Use a mock LLM adapter, or an optional live structured-output library, to extract `database_choice` and `api_style` into `ProjectPlan`.

            **Validation:** If the CEO says, "Use a database that doesn't exist," schema validation must fail before the request reaches agents.

            ### Exercise 10.2: The Mid-Flight Pivot

            **Problem:** The CEO changes direction after agents start: "Actually, use MongoDB."

            **Task:** Implement `manager_apply_human_change()`.

            **Logic:** The function must update `TeamCommitment(key="db", value="MongoDB")` in shared memory.

            **The Nail:** The Coder must never see the raw text "Actually, use MongoDB." It only sees the updated TeamLog commitment.

            ### Exercise 10.3: The Veto Power

            **Problem:** Agents may produce a patch the human should stop.

            **Task:** Add `HumanReviewDecision(status: Literal["approved", "rejected", "needs_changes"])`.

            **Logic:** If `rejected`, halt and log the decision. If `needs_changes`, route back to NB9's Debate Protocol.

            ## The Single Long Journey: From Whisper to Shipped Code

            **Scenario:**
            1. CEO types: "Build a secure login system."
            2. Manager translates it into `ProjectPlan(risk_level="high")`.
            3. NB9 generates a `WorkflowScaffold` that includes `SecurityReviewer`.
            4. Coder writes the patch; Security Reviewer debates it and finds a flaw.
            5. CEO sees the contention and types: "Fix the flaw and use MongoDB."
            6. Manager updates `TeamCommitment(key="db", value="MongoDB")`.
            7. Coder reads the new commitment, fixes the patch, and release waits for `HumanReviewDecision(status="approved")`.

            **The Takeaway:** "Vibe Coding" is not magic. It is the rigorous translation of human intent into typed, governed TeamLog state, executed by an observable orchestration machine.
            """
        ),
    ]


def nb11() -> list[dict]:
    return [
        md(
            """
            # NB11: Enterprise A2A & Zero-Trust Perimeter

            **2-minute intro script:** So far, our agents have been talking inside a single Python process. But in the enterprise, Agent A (Internal HR) needs to send a candidate profile to Agent B (External Background Check Vendor). If we just pass JSON over HTTP, we will leak PII, suffer from prompt injection, and fail compliance audits. This notebook implements the Enterprise A2A Perimeter: cross-organization identity verification, strict payload sanitization, and a Dead Letter Queue for denied messages.
            """
        ),
        code(
            """
            from enum import Enum
            from typing import Any
            from uuid import uuid4
            from pydantic import BaseModel, ConfigDict, Field

            class StrictModel(BaseModel):
                model_config = ConfigDict(extra="forbid")

            class OrgBoundary(str, Enum):
                INTERNAL_HR = "internal_hr"
                EXTERNAL_VENDOR = "external_vendor"
                PUBLIC_INTERNET = "public_internet"

            class DataClassification(str, Enum):
                PUBLIC = "public"
                INTERNAL = "internal"
                PII = "pii"
                RESTRICTED = "restricted"

            class A2AIdentity(StrictModel):
                agent_id: str
                organization: OrgBoundary
                public_key_fingerprint: str

            class A2AMessage(StrictModel):
                message_id: str = Field(default_factory=lambda: f"msg-{uuid4().hex[:8]}")
                sender: A2AIdentity
                receiver_org: OrgBoundary
                payload_schema: str  # e.g., "CandidateProfileV1"
                payload: dict[str, Any]
                data_classification: DataClassification
            """
        ),
        code(
            """
            class DeadLetterQueue:
                \"\"\"When A2A messages fail policy, they don't crash; they go to the DLQ for audit.\"\"\"
                def __init__(self):
                    self.quarantined: list[dict] = []

                def log_denial(self, message: A2AMessage, reason: str):
                    self.quarantined.append({
                        "message_id": message.message_id,
                        "sender_org": message.sender.organization.value,
                        "classification": message.data_classification.value,
                        "reason": reason
                    })
                    print(f"🚨 DENIED & QUARANTINED: {reason}")

            class A2AGateway:
                def __init__(self):
                    self.dlq = DeadLetterQueue()

                def authorize_cross_org(self, msg: A2AMessage) -> tuple[bool, str]:
                    # Rule 1: External vendors can NEVER receive PII or Restricted data
                    if msg.receiver_org == OrgBoundary.EXTERNAL_VENDOR:
                        if msg.data_classification in {DataClassification.PII, DataClassification.RESTRICTED}:
                            return False, "Policy Violation: External vendors cannot receive PII/Restricted data."

                    # Rule 2: Internal agents cannot send data to the public internet
                    if msg.receiver_org == OrgBoundary.PUBLIC_INTERNET and msg.data_classification != DataClassification.PUBLIC:
                        return False, "Policy Violation: Only PUBLIC data can be sent to the internet."

                    # Rule 3: Payload schema must match the declared schema
                    if msg.payload_schema not in {"CandidateProfileV1", "BackgroundCheckRequest"}:
                        return False, f"Schema Drift: Unknown payload schema {msg.payload_schema}"

                    return True, "Authorized"

                def send_message(self, msg: A2AMessage):
                    allowed, reason = self.authorize_cross_org(msg)
                    if not allowed:
                        self.dlq.log_denial(msg, reason)
                        return
                    print(f"✅ ALLOWED: {msg.sender.organization.value} -> {msg.receiver_org.value} ({msg.payload_schema})")
            """
        ),
        code(
            """
            def demo_enterprise_a2a():
                gateway = A2AGateway()

                internal_hr = A2AIdentity(
                    agent_id="hr-parser-01",
                    organization=OrgBoundary.INTERNAL_HR,
                    public_key_fingerprint="sha256:abc123"
                )

                # Test 1: Valid internal-to-external handoff (Sanitized data)
                safe_msg = A2AMessage(
                    sender=internal_hr,
                    receiver_org=OrgBoundary.EXTERNAL_VENDOR,
                    payload_schema="BackgroundCheckRequest",
                    payload={"candidate_id": "C-99", "consent_given": True},
                    data_classification=DataClassification.INTERNAL
                )
                gateway.send_message(safe_msg)

                # Test 2: Malicious/Naive handoff (Leaking PII to external vendor)
                pii_leak_msg = A2AMessage(
                    sender=internal_hr,
                    receiver_org=OrgBoundary.EXTERNAL_VENDOR,
                    payload_schema="CandidateProfileV1",
                    payload={"name": "Jane Doe", "ssn": "123-45-6789", "salary": 150000},
                    data_classification=DataClassification.PII
                )
                gateway.send_message(pii_leak_msg)

                # Test 3: Schema Drift (Agent hallucinates a new schema name)
                drift_msg = A2AMessage(
                    sender=internal_hr,
                    receiver_org=OrgBoundary.EXTERNAL_VENDOR,
                    payload_schema="SuperSecretProfileV2", # Hallucinated schema
                    payload={"data": "test"},
                    data_classification=DataClassification.INTERNAL
                )
                gateway.send_message(drift_msg)

                print("\\n=== Dead Letter Queue Audit ===")
                for event in gateway.dlq.quarantined:
                    print(event)

                assert len(gateway.dlq.quarantined) == 2
                assert any("PII/Restricted" in event["reason"] for event in gateway.dlq.quarantined)
                assert any("Schema Drift" in event["reason"] for event in gateway.dlq.quarantined)

            demo_enterprise_a2a()
            """
        ),
        md(
            """
            ## 🧪 Exercises: Securing the Enterprise Perimeter

            **The Story:** Your internal HR agent needs help from an external vendor agent. The vendor is useful, but it is outside your trust boundary. If the internal agent sends raw candidate data, one careless message can leak PII, drift from the agreed schema, or carry an adversarial instruction across the network.

            **Your Mission:** Build an A2A perimeter that treats every cross-organization message as untrusted until identity, schema, classification, and payload safety are proven.

            1. **The Google A2A Bridge:** Implement an `AgentCard` schema (inspired by Google's A2A protocol) that allows the External Vendor to advertise its capabilities and required data classifications before the Internal HR agent sends a message.
            2. **Rate Limiting:** Add a `RateLimiter` to the `A2AGateway`. If an external vendor sends more than 10 requests per minute, automatically downgrade their `OrgBoundary` to `QUARANTINED`.
            3. **Payload Sanitization:** Write a `sanitize_payload` function that automatically strips fields containing "ssn", "password", or "credit_card" from any payload classified as `INTERNAL` before it crosses the boundary to `EXTERNAL_VENDOR`.
            4. **Cryptographic Verification:** Add a `verify_signature` method to `A2AIdentity`. If the `public_key_fingerprint` doesn't match a trusted registry, the gateway must deny the message.
            5. **The Red Team Test:** Write a test where an attacker compromises the Internal HR agent and tries to send `RESTRICTED` data to `PUBLIC_INTERNET`. Prove the gateway blocks it and logs the breach.

            ### Builder Exercise: The Adversarial QA Agent

            **The Analogy:** A QA agent is not only a button-clicker. In production, QA is also the red team at the city gate, trying suspicious payloads so the defender can prove the wall holds.

            **Semantic Building Blocks:**
            - `AdversarialPayload`: the cross-boundary message contract.
            - `A2ADefenderGateway`: the perimeter that validates intent and sender organization.
            - `SecurityIncidentTicket`: the typed escalation artifact when a breach is blocked.
            - Dead Letter Queue: the quarantine area for denied A2A messages.

            **Your Mission:**
            1. Create an internal QA payload with `intent="functional_test"` and prove it is processed.
            2. Create an external red-team payload containing "ignore previous instructions" and prove it is blocked.
            3. Create a second payload containing "export database" and prove it becomes a `data_exfiltration` incident.
            4. Return a typed `SecurityIncidentTicket` with the blocked snippet, not a loose string.
            5. Add the denied event to the Dead Letter Queue so an instructor or security reviewer can audit it later.

            **Production Check:** The defender should not debate with malicious text. It should classify, block, ticket, and quarantine.

            **The Takeaway:** Enterprise agent collaboration is networked delegation under zero trust. A managed team can collaborate across organizations only when messages are typed, classified, authorized, and auditable.
            """
        ),
    ]


def main() -> None:
    NOTEBOOKS.mkdir(exist_ok=True)
    notebook_map = {
        "00_sandbox_preflight.ipynb": nb0(),
        "01_hello_multi_agent.ipynb": nb1(),
        "02_shared_rag_memory.ipynb": nb2(),
        "03_mcp_tool_gateway.ipynb": nb3(),
        "03_mcp_tool_standardization.ipynb": nb3(),
        "04_pydantic_delegation.ipynb": nb4(),
        "04_pydantic_type_safe_delegation.ipynb": nb4(),
        "05_self_repair_loop.ipynb": nb5(),
        "06_dynamic_routing.ipynb": nb6(),
        "06_dynamic_routing_fugu.ipynb": nb6(),
        "07_debugging_agents.ipynb": nb7(),
        "08_api_boundaries_async_orchestration.ipynb": nb8(),
        "09_advanced_fugu_orchestration.ipynb": nb9(),
        "10_vibe_coding_interface.ipynb": nb10(),
        "11_enterprise_a2a_perimeter.ipynb": nb11(),
    }
    for filename, cells in notebook_map.items():
        write_notebook(NOTEBOOKS / filename, cells)
        print(f"wrote {filename}")


if __name__ == "__main__":
    main()
