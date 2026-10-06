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
    AgentSpec("ceo", "Chief Executive Officer", "Leadership", "Lead the company and assign strategic work.", ["planning", "delegation", "review"], "idle", True, 10, "internal", 4),
    AgentSpec("ops", "Operations Manager", "Operations", "Keep the company operating smoothly and on time.", ["tracking", "scheduling", "coordination"], "idle", True, 9, "internal", 3),
    AgentSpec("research", "Research Lead", "Research", "Study targets, sources, and opportunities with evidence.", ["research", "source_review", "summaries"], "idle", True, 9, "internal", 3),
    AgentSpec("growth", "Growth Strategist", "Marketing", "Design acquisition and conversion loops.", ["research", "campaign", "content"], "idle", True, 8, "internal", 3),
    AgentSpec("sales", "Sales Manager", "Sales", "Convert leads into qualified opportunities and revenue.", ["lead_handoff", "email", "follow_up"], "idle", True, 8, "internal", 3),
    AgentSpec("product", "Product Strategist", "Product", "Translate customer needs into product action.", ["analysis", "roadmap", "prioritization"], "idle", True, 8, "internal", 3),
    AgentSpec("creative", "Creative Director", "Creative", "Create messaging, visuals, and campaign direction.", ["content", "copy", "creative"], "idle", True, 7, "internal", 3),
    AgentSpec("engineer", "Senior Engineer", "Engineering", "Build and maintain the product and automation systems.", ["build", "debug", "deploy"], "idle", True, 9, "internal", 3),
    AgentSpec("support", "Support specialist", "Support", "Handle customer communication and issue response.", ["email", "triage", "case_management"], "idle", True, 7, "internal", 3),
    AgentSpec("finance", "Finance Analyst", "Finance", "Track spending, returns, and performance trend.", ["budgeting", "reporting", "forecasting"], "idle", True, 7, "internal", 3),
]


def default_company() -> dict[str, Any]:
    return {
        "name": "AICorpOS",
        "brand": "AI company operating system",
        "objective": "Run a high-velocity AI company with research, operations, product, and communication systems.",
        "status": "running",
        "phase": "setup",
        "autonomy": True,
        "budget": 2500,
        "revenue_target": 25000,
        "cycle_interval_seconds": 180,
        "preferences": {"notify_level": "high", "risk": "medium", "max_parallel_tasks": 3},
    }


__all__ = ["AgentSpec", "DEFAULT_AGENT_SPECS", "default_company"]


path="backend/app/agents.py" 
