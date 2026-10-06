from __future__ import annotations

from typing import Any

from app.storage import JsonStore
from app.agents import DEFAULT_AGENT_SPECS, default_company


class CompanyStore:
    def __init__(self, base_dir: str = "data"):
        self.store = JsonStore(base_dir)
        self.company_key = "company"
        self.agents_key = "agents"
        self.tasks_key = "tasks"
        self.gmail_key = "gmail"
        self.research_key = "research"
        self.notifications_key = "notifications"
        self.files_key = "files"

    def ensure_seed(self) -> dict[str, Any]:
        company = self.store.load(self.company_key, None)
        if not company:
            self.store.save(self.company_key, default_company())
        agents = self.store.load(self.agents_key, None)
        if not agents:
            self.store.save(self.agents_key, [self.agent_to_dict(a) for a in DEFAULT_AGENT_SPECS])
        tasks = self.store.load(self.tasks_key, [])
        if not tasks:
            self.store.save(self.tasks_key, [])
        if self.store.load(self.notifications_key, None) is None:
            self.store.save(self.notifications_key, [])
        return self.store.load(self.company_key)

    @staticmethod
    def agent_to_dict(agent: Any) -> dict[str, Any]:
        return {
            "id": agent.id,
            "name": agent.name,
            "role": agent.role,
            "department": agent.department,
            "objective": agent.objective,
            "tools": agent.tools,
            "status": agent.status,
            "enabled": agent.enabled,
            "priority": agent.priority,
            "model": agent.model,
            "max_tasks": agent.max_tasks,
        }

    def get_company(self) -> dict[str, Any]:
        return self.store.load(self.company_key, default_company())

    def save_company(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.store.save(self.company_key, payload)
        return payload

    def list_agents(self) -> list[dict[str, Any]]:
        return self.store.load(self.agents_key, [])

    def create_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        agents = self.list_agents()
        agent_id = payload.get("id") or payload.get("name", "agent").lower().replace(" ", "-")
        record = {
            "id": agent_id,
            "name": payload["name"],
            "role": payload.get("role", "Generalist"),
            "department": payload.get("department", "Operations"),
            "objective": payload.get("objective", "Execute assigned tasks efficiently."),
            "tools": payload.get("tools", ["research", "task" ]),
            "status": "idle",
            "enabled": True,
            "priority": payload.get("priority", 5),
            "model": payload.get("model", "internal"),
            "max_tasks": payload.get("max_tasks", 2),
        }
        agents.append(record)
        self.store.save(self.agents_key, agents)
        return record

    def list_tasks(self) -> list[dict[str, Any]]:
        return self.store.load(self.tasks_key, [])

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        tasks = self.list_tasks()
        task = {
            "id": payload.get("id") or f"task-{len(tasks)+1}",
            "title": payload["title"],
            "description": payload.get("description", ""),
            "task_type": payload.get("task_type", "general"),
            "status": "queued",
            "priority": payload.get("priority", 5),
            "assignee": payload.get("assignee", "ceo"),
            "created_at": payload.get("created_at") or __import__("datetime").datetime.utcnow().isoformat(),
            "result": payload.get("result"),
            "metadata": payload.get("metadata", {}),
        }
        tasks.append(task)
        self.store.save(self.tasks_key, tasks)
        return task

    def save_tasks(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.store.save(self.tasks_key, tasks)
        return tasks

    def save_notifications(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.store.save(self.notifications_key, items)
        return items

    def list_notifications(self) -> list[dict[str, Any]]:
        return self.store.load(self.notifications_key, [])

    def set_gmail(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.store.save(self.gmail_key, payload)
        return payload

    def get_gmail(self) -> dict[str, Any]:
        return self.store.load(self.gmail_key, {"status": "disconnected", "email": None, "credentials": None})

    def set_research(self, payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.store.save(self.research_key, payload)
        return payload

    def list_research(self) -> list[dict[str, Any]]:
        return self.store.load(self.research_key, [])

    def save_files(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.store.save(self.files_key, items)
        return items

    def list_files(self) -> list[dict[str, Any]]:
        return self.store.load(self.files_key, [])
