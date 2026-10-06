from __future__ import annotations

from app.agents import DEFAULT_AGENT_SPECS, default_company
from app.storage import JsonStore


class AICorpOS:
    def __init__(self, base_dir: str = "data") -> None:
        self.store = JsonStore(base_dir)
        self.company_key = "company"
        self.agent_key = "agents"
        self.task_key = "tasks"
        self.research_key = "research"
        self.notifications_key = "notifications"
        self.files_key = "files"
        self.gmail_key = "gmail"

    def ensure_seed(self) -> dict:
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

        if self.store.load(self.task_key, None) is None:
            self.store.save(self.task_key, [])
        if self.store.load(self.notifications_key, None) is None:
            self.store.save(self.notifications_key, [])
        if self.store.load(self.files_key, None) is None:
            self.store.save(self.files_key, [])
        if self.store.load(self.gmail_key, None) is None:
            self.store.save(self.gmail_key, {"status": "disconnected"})

        return self.store.load(self.company_key)

    def get_company(self) -> dict:
        return self.store.load(self.company_key, default_company())

    def save_company(self, payload: dict) -> dict:
        current = self.get_company()
        merged = {**current, **payload}
        self.store.save(self.company_key, merged)
        return merged

    def list_agents(self) -> list[dict]:
        return self.store.load(self.agent_key, [])

    def add_agent(self, payload: dict) -> dict:
        agents = self.list_agents()
        record = {
            "id": payload.get("id") or f"agent-{len(agents)+1}",
            "name": payload["name"],
            "role": payload.get("role", "Generalist"),
            "department": payload.get("department", "Operations"),
            "objective": payload.get("objective", "Execute work efficiently."),
            "tools": payload.get("tools", ["research", "task"]),
            "status": "idle",
            "enabled": payload.get("enabled", True),
            "priority": payload.get("priority", 5),
            "model": payload.get("model", "internal"),
            "max_tasks": payload.get("max_tasks", 2),
        }
        agents.append(record)
        self.store.save(self.agent_key, agents)
        return record

    def list_tasks(self) -> list[dict]:
        return self.store.load(self.task_key, [])

    def create_task(self, payload: dict) -> dict:
        from datetime import datetime

        tasks = self.list_tasks()
        task = {
            "id": payload.get("id") or f"task-{len(tasks)+1}",
            "title": payload["title"],
            "description": payload.get("description", ""),
            "task_type": payload.get("task_type", "general"),
            "status": "queued",
            "priority": payload.get("priority", 5),
            "assignee": payload.get("assignee") or self._route_agent(payload.get("task_type", "general")),
            "created_at": payload.get("created_at") or datetime.utcnow().isoformat(),
            "result": payload.get("result"),
            "metadata": payload.get("metadata", {}),
        }
        tasks.append(task)
        self.store.save(self.task_key, tasks)
        return task

    def _route_agent(self, task_type: str) -> str:
        mapping = {
            "research": "research", "marketing": "growth", "sales": "sales",
            "engineering": "engineer", "support": "support", "finance": "finance",
            "creative": "creative", "product": "product", "ops": "ops",
            "email": "support", "analysis": "finance", "general": "ceo",
        }
        return mapping.get(task_type, "ceo")

    def run_task(self, task_id: str) -> dict:
        from datetime import datetime

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
            "body": result.get("summary", "Task finished."),
            "read": False,
        })
        return task

    def _execute_task(self, task: dict) -> dict:
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
            return {
                "summary": f"Analytical review for {task['title']} has been generated.",
                "metrics": {"revenue_signal": 12.5, "risk": "medium", "focus": "productivity"},
                "agent": assignee,
            }

        return {
            "summary": f"Task '{task['title']}' assigned to {assignee} and processed by the internal orchestration layer.",
            "notes": description or "No additional notes provided.",
            "agent": assignee,
        }

    def _research_result(self, query: str, limit: int = 3) -> list[dict]:
        try:
            import asyncio
            from app.research import search_web
            return asyncio.run(search_web(query, limit))
        except Exception:
            return [{
                "title": query,
                "url": "https://example.com",
                "snippet": "Fallback research placeholder generated locally because no external search service was available.",
            }]

    def list_research(self) -> list[dict]:
        return self.store.load(self.research_key, [])

    def save_research(self, results: list[dict]) -> list[dict]:
        self.store.save(self.research_key, results)
        return results

    def push_notification(self, notification: dict) -> dict:
        items = self.store.load(self.notifications_key, [])
        items.insert(0, notification)
        self.store.save(self.notifications_key, items[:20])
        return notification

    def list_notifications(self) -> list[dict]:
        return self.store.load(self.notifications_key, [])

    def list_files(self) -> list[dict]:
        return self.store.load(self.files_key, [])

    def save_file(self, payload: dict) -> dict:
        items = self.list_files()
        entry = {
            "id": payload.get("id") or f"file-{len(items)+1}",
            "name": payload["name"],
            "path": payload.get("path", "/tmp"),
            "content": payload.get("content", ""),
            "updated_at": payload.get("updated_at") or __import__("datetime").datetime.utcnow().isoformat(),
        }
        items.append(entry)
        self.store.save(self.files_key, items)
        return entry

    def get_dashboard(self) -> dict:
        company = self.get_company()
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
            "agents": agents[:8],
            "tasks": tasks[-5:],
            "notifications": notifications[:5],
            "resources": [
                {"name": "Google AI Studio", "url": "https://aistudio.google.com/?hl=en"},
                {"name": "OpenRouter", "url": "https://openrouter.ai"},
                {"name": "Hugging Face", "url": "https://huggingface.co"},
                {"name": "GitHub", "url": "https://github.com"},
                {"name": "YouTube API Docs", "url": "https://developers.google.com/youtube"},
                {"name": "Gmail API Docs", "url": "https://developers.google.com/gmail/api"},
            ],
        }

    def get_gmail(self) -> dict:
        return self.store.load(self.gmail_key, {"status": "disconnected"})

    def set_gmail(self, payload: dict) -> dict:
        self.store.save(self.gmail_key, payload)
        return payload

    def get_resources(self) -> list[dict]:
        return [
            {"name": "AICorpOS resources", "type": "internal", "url": "https://github.com/dengesiz26-crypto/ai-company-independent"},
            {"name": "Google AI Studio", "url": "https://aistudio.google.com/?hl=en"},
            {"name": "OpenRouter", "url": "https://openrouter.ai"},
            {"name": "Hugging Face", "url": "https://huggingface.co"},
            {"name": "GitHub", "url": "https://github.com"},
            {"name": "Google Developers", "url": "https://developers.google.com"},
        ]


engine = AICorpOS("data")


async def bootstrap() -> None:
    engine.ensure_seed()


async def run_manager_cycle() -> dict:
    company = engine.get_company()
    tasks = engine.list_tasks()
    if not tasks:
        task = engine.create_task({
            "title": "Launch company operations system",
            "description": "Initialize company dashboard, research, and communication systems.",
            "task_type": "general",
            "assignee": "ceo",
        })
        engine.run_task(task["id"])
        return {"status": "created", "task": task}
    return {"status": "ok", "queued": len(tasks), "company": company["name"]}


__all__ = ["engine", "bootstrap", "run_manager_cycle"]


path="backend/app/engine.py"
