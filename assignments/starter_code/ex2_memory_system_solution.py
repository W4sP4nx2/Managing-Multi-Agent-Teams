"""Instructor solution for Ex2: Theory-of-Mind Memory System.

Run:
    python3 assignments/starter_code/ex2_memory_system_solution.py
"""

from enum import Enum
from typing import List, Set
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Role(str, Enum):
    PM = "pm"
    CODER = "coder"
    SECURITY = "security"
    QA = "qa"


class Sensitivity(str, Enum):
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MemoryRecord(StrictModel):
    author: Role
    visible_to: Set[Role]
    sensitivity: Sensitivity
    tags: Set[str]
    text: str
    record_id: str = Field(default_factory=lambda: f"mem_{uuid4().hex[:8]}")


class DesignPlan(StrictModel):
    storage_choice: str
    rationale: str
    risks: List[str] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)


class SharedMemory:
    def __init__(self) -> None:
        self.records: List[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> str:
        self.records.append(record)
        return record.record_id

    def search(self, query: str, requester: Role) -> List[MemoryRecord]:
        query_lower = query.lower()
        results: List[MemoryRecord] = []

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


def coder_create_design(prompt: str, memory: SharedMemory) -> DesignPlan:
    records = memory.search("storage", Role.CODER)
    for record in records:
        if "postgresql" in record.text.lower():
            return DesignPlan(
                storage_choice="PostgreSQL",
                rationale=f"Found PM architecture constraint in {record.record_id}.",
                risks=["Migration design required", "Backups and connection pooling must be specified"],
                follow_up_questions=["What retention policy should the database use?"],
            )

    return DesignPlan(
        storage_choice="Unknown",
        rationale=f"No storage constraint found for prompt: {prompt}",
        risks=["Implementation may violate architecture expectations"],
    )


def demo_theory_of_mind() -> None:
    memory = SharedMemory()
    memory.add(
        MemoryRecord(
            author=Role.PM,
            visible_to={Role.CODER, Role.QA, Role.SECURITY},
            sensitivity=Sensitivity.CONFIDENTIAL,
            tags={"architecture", "storage", "constraint"},
            text="Use PostgreSQL for persistent storage. Do not use SQLite.",
        )
    )
    memory.add(
        MemoryRecord(
            author=Role.SECURITY,
            visible_to={Role.SECURITY},
            sensitivity=Sensitivity.RESTRICTED,
            tags={"credentials"},
            text="Production DB password: super_secret_123",
        )
    )

    design = coder_create_design("Implement the user persistence layer.", memory)
    assert design.storage_choice == "PostgreSQL"
    assert memory.search("credentials", Role.CODER) == []
    assert len(memory.search("credentials", Role.SECURITY)) == 1

    print(design.model_dump_json(indent=2))
    print("Coder credential search:", len(memory.search("credentials", Role.CODER)))
    print("Security credential search:", len(memory.search("credentials", Role.SECURITY)))


if __name__ == "__main__":
    demo_theory_of_mind()
