from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from app.agents import DEFAULT_AGENT_SPECS, default_company
from app.storage import JsonStore
from app.research import search_web, read_page


class AICorpOS:
    def __init__(self, base_dir: str = "data") -> None:
        self.store = JsonStore(base_dir)
        self.company_key = "company"
        self.agent_key = "agents"
        self.task_key = "tasks"
        self.research_key = "research"
        self.notifications_key = "notifications"

    def ensure_seed(self) -> dict[str, Any]:
        company = self.store.load(self.company_key, None)
        if company is None:
            company = default_company()
            self.store.save(self.company_key, company)
        agents = self.store.load(self.agent_key, None)
        if agents is None:
            agents = [
                {
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
                for agent in DEFAULT_AGENT_SPECS
            ]
            self.store.save(self.agent_key, agents)
        tasks = self.store.load(self.task_key, [])
        if tasks is None:
            self.store.save(self.task_key, [])
        notifications = self.store.load(self.notifications_key, [])
        if notifications is None:
            self.store.save(self.notifications_key, [])
        return self.store.load(self.company_key)

    def create_or_update_company(self, payload: dict[str, Any]) -> dict[str, Any]:
        current = self.store.load(self.company_key, default_company())
        merged = {**current, **payload}
        self.store.save(self.company_key, merged)
        return merged

    def list_agents(self) -> list[dict[str, Any]]:
        return self.store.load(self.agent_key, [])

    def add_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        agents = self.list_agents()
        record = {
            "id": payload.get("id") or f"agent-{len(agents)+1}",
            "name": payload["name"],
            "role": payload.get("role", "Generalist"),
            "department": payload.get("department", "Operations"),
            "objective": payload.get("objective", "Execute the assigned work efficiently."),
            "tools": payload.get("tools", ["research", "analysis"]),
            "status": "idle",
            "enabled": True,
            "priority": payload.get("priority", 5),
            "model": payload.get("model", "internal"),
            "max_tasks": payload.get("max_tasks", 2),
        }
        agents.append(record)
        self.store.save(self.agent_key, agents)
        return record

    def list_tasks(self) -> list[dict[str, Any]]:
        return self.store.load(self.task_key, [])

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        tasks = self.list_tasks()
        task = {
            "id": payload.get("id") or f"task-{len(tasks)+1}",
            "title": payload["title"],
            "description": payload.get("description", ""),
            "task_type": payload.get("task_type", "general"),
            "status": "queued",
            "priority": payload.get("priority", 5),
            "assignee": payload.get("assignee") or self._route_agent(payload["task_type"]),
            "metadata": payload.get("metadata", {}),
            "created_at": datetime.utcnow().isoformat(),
            "result": None,
        }
        tasks.append(task)
        self.store.save(self.task_key, tasks)
        return task

    def _route_agent(self, task_type: str) -> str:
        mapping = {
            "research": "research",
            "marketing": "growth",
            "sales": "sales",
            "engineering": "engineer",
            "support": "support",
            "finance": "finance",
            "creative": "creative",
            "product": "product",
            "ops": "ops",
        }
        return mapping.get(task_type, "ceo")

    def run_task(self, task_id: str) -> dict[str, Any]:
        tasks = self.list_tasks()
        task = next((item for item in tasks if item["id"] == task_id), None)
        if task is None:
            raise ValueError("Task not found")

        task["status"] = "running"
        self.store.save(self.task_key, tasks)

        result = self._execute_task(task)
        task["result"] = result
        task["status"] = "completed"
        task["completed_at"] = datetime.utcnow().isoformat()
        self.store.save(self.task_key, tasks)
        self.push_notification({
            "id": f"notif-{datetime.utcnow().timestamp()}",
            "type": "task_completed",
            "title": f"Task completed: {task['title']}",
            "body": result["summary"],
            "read": False,
        })
        return task

    def _execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
        task_type = task.get("task_type", "general")
        description = task.get("description", "")
        assignee = task.get("assignee", "ceo")

        if task_type == "research":
            query = description or task["title"]
            results = self._research_result(query)
            summary = f"Research completed for '{query}'. Found {len(results)} sources."
            return {"summary": summary, "results": results, "agent": assignee}

        if task_type == "email":
            return {
                "summary": f"Email workflow prepared for {assignee}.",
                "draft": {
                    "subject": task["title"],
                    "body": description or "Hello, here is the draft response.",
                },
                "agent": assignee,
            }

        if task_type == "analysis":
            metrics = {
                "revenue_signal": 12.5,
                "risk": "medium",
                "focus": "productivity",
            }
            return {"summary": f"Analytical review for {task['title']} has been generated.", "metrics": metrics, "agent": assignee}

        return {
            "summary": f"Task '{task['title']}' assigned to {assignee} and processed by the internal orchestration layer.",
            "notes": description or "No additional notes provided.",
            "agent": assignee,
        }

    def _research_result(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        results = []
        try:
            import asyncio
            results = asyncio.run(search_web(query, limit))
        except Exception:
            return [{
                "title": query,
                "url": "https://example.com",
                "snippet": "Fallback research placeholder generated locally because no external search service was available.",
            }]
        return results

    def list_research(self) -> list[dict[str, Any]]:
        return self.store.load(self.research_key, [])

    def save_research(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.store.save(self.research_key, results)
        return results

    def push_notification(self, notification: dict[str, Any]) -> dict[str, Any]:
        items = self.store.load(self.notifications_key, [])
        items.insert(0, notification)
        self.store.save(self.notifications_key, items[:20])
        return notification

    def list_notifications(self) -> list[dict[str, Any]]:
        return self.store.load(self.notifications_key, [])

    def dashboard(self) -> dict[str, Any]:
        company = self.store.load(self.company_key, default_company())
        agents = self.list_agents()
        tasks = self.list_tasks()
        notifications = self.list_notifications()
        return {
            "company": company,
            "stats": {
                "agents": len(agents),
                "tasks_total": len(tasks),
                "tasks_completed": sum(1 for t in tasks if t.get("status") == "completed"),
                "tasks_queued": sum(1 for t in tasks if t.get("status") == "queued"),
                "notifications": len(notifications),
            },
            "agents": agents,
            "tasks": tasks[-10:],
            "notifications": notifications[:5],
        }


engine = AICorpOS("data")


async def bootstrap() -> None:
    engine.ensure_seed()
