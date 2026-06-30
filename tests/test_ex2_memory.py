from __future__ import annotations

from assignments.starter_code.ex2_memory_system_solution import (
    MemoryRecord,
    Role,
    Sensitivity,
    SharedMemory,
    coder_create_design,
)


def test_coder_discovers_postgresql_constraint() -> None:
    """Verify the coder finds PM's hidden-but-authorized storage constraint."""

    memory = SharedMemory()
    memory.add(
        MemoryRecord(
            author=Role.PM,
            visible_to={Role.CODER},
            sensitivity=Sensitivity.CONFIDENTIAL,
            tags={"architecture", "storage"},
            text="Use PostgreSQL for persistent storage.",
        )
    )

    design = coder_create_design("Implement persistence", memory)
    assert design.storage_choice == "PostgreSQL"
    assert "PM architecture constraint" in design.rationale


def test_coder_cannot_read_security_password() -> None:
    """Verify shared memory is governed memory, not open memory."""

    memory = SharedMemory()
    memory.add(
        MemoryRecord(
            author=Role.SECURITY,
            visible_to={Role.SECURITY},
            sensitivity=Sensitivity.RESTRICTED,
            tags={"credentials"},
            text="Production DB password: super_secret_123",
        )
    )

    assert memory.search("password", Role.CODER) == []
    assert len(memory.search("password", Role.SECURITY)) == 1
