# %% {"id": "bonus-intro", "type": "markdown"}
# # Bonus live LLM demo — end of Day 2
#
# **Instructor only, optional, ungraded.** Complete the core labs and Capstone ADR first. This notebook illustrates one real response constrained by a Pydantic contract. It is isolated from the five required notebooks and their graders.
#
# Use the separate optional environment described in [SETUP.md](../SETUP.md) and install `requirements/live-llm.txt`. A network connection and your own `OPENAI_API_KEY` are required only when you deliberately enable the flag below. Live calls may incur charges. Never paste a key into the notebook. Inspect the response and explain that schema validity does not prove the answer is correct.

# API reference: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat) documents the Pydantic `response_format` and `.parsed` result used below.

# %% {"id": "bonus-config", "type": "code"}
import os
from pydantic import BaseModel, ConfigDict, Field

USE_LIVE_LLM = False

class ResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    findings: list[str]

# %% {"id": "bonus-live-call", "type": "code"}
if USE_LIVE_LLM:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in the shell before starting this optional demo.")
    from openai import OpenAI

    client = OpenAI()
    completion = client.chat.completions.parse(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Give two brief API security practices and a confidence score from 0 to 1."}],
        response_format=ResearchOutput,
    )
    result = completion.choices[0].message.parsed
    if result is None:
        raise RuntimeError("The provider did not return a structured result; inspect the response.")
    print(result.model_dump_json(indent=2))
else:
    print("Demo disabled. The required course remains fully offline.")
