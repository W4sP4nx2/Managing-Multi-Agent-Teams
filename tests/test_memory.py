from __future__ import annotations

from src.enterprise_agent_team import (
    AgentIdentity,
    AgentRole,
    MemoryRecord,
    SharedAgenticMemory,
    TrustTier,
)


def test_memory_visibility_by_sensitivity() -> None:
    memory = SharedAgenticMemory()
    memory.add(
        MemoryRecord(
            text="Public design note",
            tags={"design"},
            sensitivity=TrustTier.PUBLIC,
            author=AgentRole.PRODUCT_MANAGER,
        )
    )
    memory.add(
        MemoryRecord(
            text="Production DB password: super_secret",
            tags={"credentials"},
            sensitivity=TrustTier.RESTRICTED,
            author=AgentRole.SECURITY_REVIEWER,
        )
    )

    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes=set(),
        clearance=TrustTier.CONFIDENTIAL,
    )

    public_results = memory.search("design", coder)
    assert len(public_results) == 1
    assert "Public design note" in public_results[0].text

    restricted_results = memory.search("password", coder)
    assert restricted_results == []


def test_restricted_memory_visible_to_restricted_identity() -> None:
    memory = SharedAgenticMemory()
    memory.add(
        MemoryRecord(
            text="Production DB password: super_secret",
            tags={"credentials"},
            sensitivity=TrustTier.RESTRICTED,
            author=AgentRole.SECURITY_REVIEWER,
        )
    )
    security = AgentIdentity(
        agent_id="security-001",
        role=AgentRole.SECURITY_REVIEWER,
        org_id="training",
        scopes=set(),
        clearance=TrustTier.RESTRICTED,
    )

    results = memory.search("credentials", security)
    assert len(results) == 1
    assert "password" in results[0].text.lower()

