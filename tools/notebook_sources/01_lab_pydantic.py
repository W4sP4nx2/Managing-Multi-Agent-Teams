# %% {"id": "lab1-hook", "type": "markdown"}
# <a id="lab1-start"></a>
# ## Lab 1 — Context Engineering: Typed Contracts
#
# **Navigate:** [Flow map](#lab1-flow-map) → [Observe](#lab1-observe) → [Repair](#lab1-repair) → [Grade](#lab1-evidence) → [Explain the result](#lab1-transfer) → [Lab 2](02_lab_crewai.ipynb).
#
# [Course home](../README.md) · [Assignment 03 and pass criteria](../ASSIGNMENTS.md#assignment-03-architectural-supervision)
#
# ## What you interact with
#
# | Action | Your next step | Expected result |
# | --- | --- | --- |
# | **Run** | Run the supplied weak-model cell. | It accepts an impossible confidence score and ignores an undeclared field. |
# | **Edit** | Complete the three TODOs in `StrictResearchOutput`. | Required fields, an inclusive `0.0–1.0` range, and an extra-field rejection policy are declared. |
# | **Inspect** | Run the unchanged grader and read both scored checks. | Valid inputs pass; malformed fields and scores are rejected. |
# | **Finish** | Reach **15/15** and state one property the schema cannot verify. | Keep the grader output for Assignment 03, then open Lab 2. |
#
# You are editing and validating a Python data contract. `MOCK_LLM_RESPONSE` is a fixed local dictionary; no agent team or model runs. This contract represents the Coder-to-QA handoff you configure in Lab 2.
#
# **Predict:** which two parts of the response should a strict contract reject?

# %% {"id": "lab1-flow-map", "type": "markdown", "diagram": "resources/diagrams/lab1-contract-flow.svg"}
# <a id="lab1-flow-map"></a>
# ### Flow map · the contract you will repair
#
# ![Lab 1 exercise: inspect the weak model, edit StrictResearchOutput, and run acceptance and rejection probes.](attachment:lab1-contract-flow.svg)
#
# **Read the flow:** the supplied dictionary passes `WeakResearchOutput`. You edit only `StrictResearchOutput`; the grader then calls `model_validate()` with valid and malformed probes. Accepted probes produce a typed object; rejected probes raise a validation error. These checks report **15 points**.
#
# The diagram describes this notebook's local validation path. It does not show executed Coder or QA agents. A valid schema result establishes tested structure and bounds; it does not establish factual correctness.
#
# <a id="lab1-observe"></a>
# ### 1 · Run and inspect the weak model
#
# Run the next code cell. Find `confidence_score=150.5` in the accepted model and notice that `secret_backdoor` disappeared.

# %% {"id": "lab1-broken-state", "type": "code"}
USE_LIVE_LLM = False

from pydantic import BaseModel

# Deterministic mock of a flawed model response. No live API is called.
MOCK_LLM_RESPONSE = {
    "topic": "API Security",
    "confidence_score": 150.5,  # Invalid: the allowed range is 0.0 to 1.0.
    "findings": ["Use HTTPS for all API traffic."],
    "secret_backdoor": True,    # Invalid: this field is not in the contract.
}


class WeakResearchOutput(BaseModel):
    """Intentionally weak contract for the starting exercise."""

    topic: str
    confidence_score: float
    findings: list[str]
    # Pydantic's default extra-field behavior is "ignore".
    # There is no constraint on the confidence score.


# This succeeds without a ValidationError, despite the bad score and extra field.
# In Jupyter, the last expression displays the accepted model.
WEAK_RESULT = WeakResearchOutput.model_validate(MOCK_LLM_RESPONSE)
WEAK_RESULT

# %% {"id": "lab1-mission", "type": "markdown"}
# <a id="lab1-repair"></a>
# ### 2 · Edit the strict contract
#
# Complete the three TODOs in the next code cell:
#
# 1. Require `topic: str`, `confidence_score: float`, and `findings: list[str]`.
# 2. Set the inclusive range `0.0 <= confidence_score <= 1.0`.
# 3. Forbid undeclared fields such as `secret_backdoor`.
#
# Run your model cell, then the supplied grader. A correctly shaped response must still pass. Do not change the fixture or grader to make the exercise pass.

# %% {"id": "lab1-learner-workspace", "type": "code"}
from pydantic import BaseModel, ConfigDict, Field


class StrictResearchOutput(BaseModel):
    """TODO: define the strict research-output contract."""

    # TODO: Forbid extra fields with Pydantic v2 model configuration.
    # TODO: Declare the required topic and findings fields.
    # TODO: Constrain confidence_score to the inclusive range 0.0–1.0.
    pass

# %% {"id": "lab1-evidence-guide", "type": "markdown"}
# <a id="lab1-evidence"></a>
# ### 3 · Check acceptance and rejection evidence
#
# Run the grader after editing the contract. A repaired gate must admit the valid probe and both boundary values (`0.0`, `1.0`), then reject the malformed probes. Read each result before accepting the **15/15** total.
#
# | Evidence | Meaning for the handoff |
# | --- | --- |
# | Valid required fields accepted | QA can consume a correctly shaped artifact. |
# | Out-of-range scores rejected · 5 points | The confidence value meets the declared numeric bounds. |
# | Undeclared fields rejected · 10 points | Unexpected fields cannot cross this contract boundary. |
#
# Required fields and basic type checks are prerequisites for both scored gates. Record the grader output and one limitation of this evidence in your working brief.

# %% {"id": "lab1-auto-grader", "type": "code"}
from pydantic import BaseModel

StrictModel = globals().get("StrictResearchOutput")
MockResponse = globals().get("MOCK_LLM_RESPONSE")
lab1_score = 0

if not isinstance(StrictModel, type) or not issubclass(StrictModel, BaseModel):
    print("❌ 0/15 — Define StrictResearchOutput as a Pydantic model.")
elif not isinstance(MockResponse, dict):
    print("❌ 0/15 — Rerun the deterministic fixture cell before grading.")
else:
    valid_probe = {"topic": "API Security", "confidence_score": 0.95,
                   "findings": ["Use HTTPS for all API traffic."]}

    def is_accepted(payload: dict) -> bool:
        try:
            StrictModel.model_validate(payload)
            return True
        except Exception:
            return False

    required_fields = {"topic", "confidence_score", "findings"}
    shape_ok = (
        set(StrictModel.model_fields) == required_fields
        and all(field.is_required() for field in StrictModel.model_fields.values())
        and is_accepted(valid_probe)
        and all(not is_accepted({key: value for key, value in valid_probe.items()
                                 if key != missing}) for missing in required_fields)
        and not is_accepted({**valid_probe, "topic": ["wrong type"]})
        and not is_accepted({**valid_probe, "findings": "wrong type"})
    )
    range_ok = (
        shape_ok
        and is_accepted({**valid_probe, "confidence_score": 0.0})
        and is_accepted({**valid_probe, "confidence_score": 1.0})
        and not is_accepted({**valid_probe, "confidence_score": -0.01})
        and not is_accepted({**valid_probe, "confidence_score": 150.5})
    )
    extras_ok = shape_ok and not is_accepted({**valid_probe, "secret_backdoor": True})
    lab1_score = (5 if range_ok else 0) + (10 if extras_ok else 0)
    print(f"{'✅' if range_ok else '❌'} [{5 if range_ok else 0}/5] Inclusive score range 0.0–1.0")
    print(f"{'✅' if extras_ok else '❌'} [{10 if extras_ok else 0}/10] Undeclared fields rejected")
    if not shape_ok:
        print("Declare required topic: str, confidence_score: float, and findings: list[str]; accept valid input.")
    if not range_ok:
        print("Set confidence_score: float = Field(ge=0.0, le=1.0).")
    if not extras_ok:
        print('Set model_config = ConfigDict(extra="forbid").')
    print(f"LAB 1 SCORE: {lab1_score}/15")
    if lab1_score == 15:
        print("✅ SUCCESS: 15/15 — stop here and move to Lab 2.")

# %% {"id": "lab1-live-factory-transfer", "type": "markdown"}
# <a id="lab1-transfer"></a>
# ## Explain the result
#
# After reaching **15/15**, write one sentence naming the rejected fields or values and one sentence naming a claim the schema did not check. For example, the schema cannot establish that a finding is factually correct.
#
# Keep this note with your grader output for [Assignment 03](../ASSIGNMENTS.md#assignment-03-architectural-supervision). Continue to Lab 2 to configure which role may create and review the artifact.
#
# [Back to the flow map](#lab1-flow-map)

# %% {"id": "learner-navigation-01", "type": "markdown"}
# ## Continue or return
#
# After completing this notebook and inspecting its evidence, continue to [Lab 2](02_lab_crewai.ipynb).
#
# [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index) · [Practical sequence](../README.md#required-practical-sequence)
