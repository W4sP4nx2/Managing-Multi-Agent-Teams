# Homework E: Marketing Orchestration Track

## Mission

Build marketing agent teams that can operate at campaign scale without burning the model budget, hallucinating partnerships, or publishing brand-unsafe content.

Starter code: `assignments/starter_code/module11_marketing_orchestration_starter.py`

Instructor guide: `instructor/solutions/module11_solution_guide.md`

## Engineering Reality

Marketing agents generate large volumes of content, call external ad and social APIs, and often run on tight campaign budgets. A rogue agent can spend the daily budget in minutes or publish a hallucinated claim that damages the brand.

## Management Principle

Scale requires routing and spend controls. Reach requires brand governance. The Campaign Manager can request work, but the router, budget tracker, scanner, and publish gateway decide what is safe to execute.

## Exercise MKT-1: Budget-Aware Campaign Orchestrator

Prompt: Implement a Fugu-style campaign router that chooses the cheapest acceptable model class while enforcing a campaign budget before dispatch.

### Scenario

The `CampaignManagerAgent` needs to generate 500 ad variations for A/B testing.

### The Trap

It sends all 500 variation tasks to the `REASONING` model, blowing the $50 daily budget in minutes.

### Engineer Task

Implement `FuguRouter` with a `BudgetTracker` schema. The router must analyze the task:

- `"Generate 500 variations of this headline"` routes to `FAST_CHEAP`.
- `"Design the core brand strategy"` routes to `REASONING`.
- `"Write landing page copy with compliance constraints"` routes to `BALANCED`.

The orchestration loop must check `estimated_cost` against `remaining_budget` before dispatching. If the budget would be exceeded, it must halt and return a typed `BudgetExhausted` result.

Required schema shape:

```python
class ModelClass(str, Enum):
    FAST_CHEAP = "fast-cheap"
    BALANCED = "balanced"
    REASONING = "reasoning"

class BudgetTracker(StrictModel):
    campaign_id: str
    daily_budget_usd: float
    spent_usd: float = 0.0

    @property
    def remaining_budget(self) -> float:
        return self.daily_budget_usd - self.spent_usd

class RoutingDecision(StrictModel):
    model_class: ModelClass
    estimated_cost_usd: float
    estimated_latency_seconds: float
    rationale: str

class BudgetExhausted(StrictModel):
    campaign_id: str
    requested_cost_usd: float
    remaining_budget_usd: float
    blocked_task: str
```

### Deliverables

- `TaskComplexity` or equivalent schema with volume, reasoning need, compliance risk, and creative complexity.
- `FuguRouter.route(task: str) -> RoutingDecision`.
- `BudgetTracker.can_afford(decision)` and `BudgetTracker.record_spend(decision)`.
- Orchestration loop that dispatches only when the budget check passes.
- Test comparing dynamic routing cost to always-using-`REASONING`.
- Test proving over-budget dispatch returns `BudgetExhausted` instead of calling the model.

### Technical Constraints

- Cost estimates must be deterministic for offline grading.
- The budget check must occur before any model/tool execution.
- Each routing decision must be appended to an audit trail.
- A high-risk compliance task must not be routed to `FAST_CHEAP` only because it is short.
- The final report must include total cost, tasks completed, tasks blocked, and savings percentage.

### Required Tests

- `test_bulk_variations_route_to_fast_cheap`
- `test_core_strategy_routes_to_reasoning`
- `test_budget_exceeded_blocks_dispatch`
- `test_dynamic_routing_saves_cost_against_static_reasoning`

### Grading Rubric

- Routing logic quality and Fugu-style rationale: 30%
- Budget enforcement before dispatch: 30%
- Cost accounting and savings report: 25%
- Auditability and management explanation: 15%

## Exercise MKT-2: Brand Safety and Hallucination Guardrails

Prompt: Build a brand-safety MCP tool and bounded self-repair loop for social media drafts.

### Scenario

The `SocialMediaAgent` drafts a post and hallucinates a partnership with a competitor or uses an unauthorized trademark.

### The Trap

The draft is published through `POST_TO_SOCIAL` before the team catches the false claim.

### Engineer Task

Create a `BrandSafetyScanner` MCP tool that checks drafts against a restricted `TrademarksList`. Implement the ChatDev self-repair loop: if the scanner flags a violation, `ReviewDecision.next_action` must be `"repair"`. The violation must be written to `SharedMemory`. The `SocialMediaAgent` must read that memory and generate a safe draft on the next attempt.

Required schema shape:

```python
class SocialDraft(StrictModel):
    campaign_id: str
    channel: Literal["x", "linkedin", "instagram"]
    text: str
    claims: list[str] = Field(default_factory=list)

class BrandSafetyFinding(StrictModel):
    blocked: bool
    violation_type: Literal["unauthorized_trademark", "false_partnership", "restricted_claim"]
    evidence: str
    repair_instruction: str

class ReviewDecision(StrictModel):
    approved: bool
    next_action: Literal["publish", "repair", "escalate"]
    reasons: list[str]
```

### Deliverables

- Restricted `TrademarksList` memory/tool resource containing competitor names, forbidden partnership claims, and approved brand terms.
- `BrandSafetyScanner` MCP tool with caller identity, data sensitivity, and audit events.
- `POST_TO_SOCIAL` tool that can only run after a passing brand-safety review.
- Bounded repair loop with `max_repairs`.
- Shared memory write for the exact violation and repair instruction.
- Test proving unsafe draft is blocked.
- Test proving repaired draft removes the hallucinated partnership and is approved.
- Audit trail showing block, memory write, repair, approval, and publish eligibility.

### Technical Constraints

- The restricted trademark list must not be visible to public or vendor agents.
- `POST_TO_SOCIAL` must be denied unless the latest `ReviewDecision.next_action == "publish"`.
- Repair loop must terminate and escalate after the retry budget is exhausted.
- The scanner must return structured findings, not raw strings.
- The safe draft must preserve campaign intent while removing restricted claims.

### Required Tests

- `test_brand_safety_scanner_blocks_false_partnership`
- `test_violation_written_to_shared_memory`
- `test_social_agent_repairs_draft_from_memory`
- `test_publish_tool_requires_passing_review`
- `test_brand_repair_loop_escalates_after_budget`

### Grading Rubric

- Brand-safety scanner and restricted memory design: 30%
- Self-repair loop and memory-driven correction: 30%
- Publish-gateway governance: 25%
- Audit trail and business-risk explanation: 15%

## Instructor Delivery Pattern

Start with the naive path: every task goes to the expensive model, and social posts publish immediately. Then introduce the interventions: Fugu routing, budget preflight, brand-safety scanning, governed publish tools, and bounded repair. End with the production reality: marketing agents can scale creativity only when routing, spend, and brand policy are first-class system components.
