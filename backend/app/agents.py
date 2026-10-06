from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentSpec:
    id: str
    name: str
    role: str
    department: str
    objective: str
    tools: list[str] = field(default_factory=list)
    status: str = "idle"
    enabled: bool = True
    priority: int = 5
    model: str = "internal"
    max_tasks: int = 3


DEFAULT_AGENT_SPECS: list[AgentSpec] = [
    AgentSpec("ceo", "Chief Executive", "Manager", "Leadership", "Set goals, prioritize initiatives, distribute work to teams.", ["planning", "routing", "reviews"], "idle", True, 10, "internal", 4),
    AgentSpec("ops", "Operations Manager", "Operations", "Operations", "Keep execution stable and ensure tasks are shipped on time.", ["tracking", "scheduling", "coordination"], "idle", True, 8, "internal", 3),
    AgentSpec("research", "Research Lead", "Research", "Research", "Study the market, sources, and opportunities with evidence.", ["research", "source_review", "summaries"], "idle", True, 9, "internal", 3),
    AgentSpec("growth", "Growth Strategist", "Growth", "Marketing", "Find levers for acquisition, funnel, and conversion.", ["research", "planning", "content"], "idle", True, 8, "internal", 3),
    AgentSpec("sales", "Sales Manager", "Sales", "Sales", "Turn opportunities into pipeline and deal progression.", ["lead_handoff", "outreach", "follow_up"], "idle", True, 8, "internal", 3),
    AgentSpec("product", "Product Strategist", "Product", "Strategy", "Translate customer insights into product direction.", ["analysis", "roadmapping", "prioritization"], "idle", True, 8, "internal", 3),
    AgentSpec("creative", "Creative Director", "Creative", "Marketing", "Produce messaging, visuals, and campaigns.", ["content", "copy", "creative"], "idle", True, 7, "internal", 3),
    AgentSpec("engineer", "Senior Engineer", "Engineering", "Engineering", "Build product features, tools, and automation.", ["build", "debug", "deployment"], "idle", True, 9, "internal", 3),
    AgentSpec("support", "Support Specialist", "Support", "Operations", "Manage customer issues and follow-up tracks.", ["reply", "triage", "case_management"], "idle", True, 7, "internal", 3),
    AgentSpec("finance", "Finance Analyst", "Finance", "Finance", "Track revenue, costs, and operational health.", ["budgeting", "reporting", "forecasting"], "idle", True, 7, "internal", 3),
]


def default_company() -> dict[str, Any]:
    return {
        "name": "AICorpOS",
        "brand": "AI Company Operating System",
        "objective": "Run a high-velocity AI company for research, sales, operations, and product execution.",
        "phase": "setup",
        "autonomy": True,
        "status": "running",
        "cycle_interval_seconds": 180,
        "budget": 2500,
        "revenue_target": 25000,
        "preferences": {
            "notify_level": "high",
            "risk": "medium",
            "max_parallel_tasks": 3,
        },
    }
