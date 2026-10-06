from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CompanyInput(BaseModel):
    name: str | None = None
    objective: str | None = None
    autonomy: bool = True
    status: str = "running"
    budget: float | None = None
    revenue_target: float | None = None


class AgentInput(BaseModel):
    name: str
    role: str = "Generalist"
    department: str = "Operations"
    objective: str | None = None
    tools: list[str] = Field(default_factory=list)
    priority: int = 5


class TaskInput(BaseModel):
    title: str
    description: str = ""
    task_type: str = "general"
    priority: int = 5
    assignee: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class GmailConfigInput(BaseModel):
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str | None = None


class ResearchInput(BaseModel):
    query: str
    mode: str = "market"


path="backend/app/schemas.py" 
