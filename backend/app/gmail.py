from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentRole:
    id: str
    name: str
    department: str
    objective: str
    tools: list[str] = field(default_factory=list)
    priority: int = 5


DEFAULT_ROLES = [
    AgentRole("ceo", "Executive Director", "Leadership", "Coordinate the company and route tasks intelligently.", ["planning", "delegation", "review"], 10),
    AgentRole("ops", "Operations Manager", "Operations", "Keep daily execution stable and measurable.", ["tracking", "scheduling", "coordination"], 9),
    AgentRole("research", "Research Lead", "Research", "Gather market and competitor intelligence.", ["research", "web_search", "source_review"], 9),
    AgentRole("growth", "Growth Strategist", "Marketing", "Design growth loops and conversion strategy.", ["research", "campaign", "content"], 8),
    AgentRole("sales", "Sales Manager", "Sales", "Convert interested leads into revenue.", ["lead_handoff", "email", "follow_up"], 8),
    AgentRole("product", "Product Strategist", "Product", "Turn insights into product direction.", ["analysis", "roadmap", "prioritization"], 8),
    AgentRole("creative", "Creative Director", "Creative", "Shape brand, content, messaging, and creative assets.", ["content", "brand", "asset_creation"], 7),
    AgentRole("engineer", "Senior Engineer", "Engineering", "Ship, maintain, and improve technical systems.", ["build", "debug", "deploy"], 9),
    AgentRole("support", "Support Specialist", "Support", "Handle customer and partner communication.", ["email", "triage", "case_management"], 7),
    AgentRole("finance", "Finance Analyst", "Finance", "Monitor budget, performance, and spending.", ["budgeting", "reporting", "forecasting"], 7),
]


def get_default_roles() -> list[dict]:
    return [
        {
            "id": role.id,
            "name": role.name,
            "department": role.department,
            "objective": role.objective,
            "tools": role.tools,
            "priority": role.priority,
            "status": "idle",
        }
        for role in DEFAULT_ROLES
    ]


__all__ = ["DEFAULT_ROLES", "get_default_roles"]


path="backend/app/agent_runtime.py" 
