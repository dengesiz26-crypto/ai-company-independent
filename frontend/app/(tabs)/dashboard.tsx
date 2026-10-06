from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.engine import engine, run_manager_cycle
from app.gmail import build_oauth_url, exchange_code, list_gmail_messages, send_gmail_message
from app.research import read_page, search_web
from app.schemas import AgentInput, CompanyInput, GmailConfigInput, ResearchInput, TaskInput

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, Any]:
    return {"ok": True, "service": "AICorpOS"}


@router.get("/dashboard")
async def dashboard() -> dict[str, Any]:
    return engine.get_dashboard()


@router.get("/company")
async def get_company() -> dict[str, Any]:
    return engine.ensure_seed()


@router.post("/company")
async def create_company(payload: CompanyInput) -> dict[str, Any]:
    return engine.save_company(payload.model_dump(exclude_none=True))


@router.get("/agents")
async def list_agents() -> list[dict[str, Any]]:
    return engine.list_agents()


@router.post("/agents")
async def create_agent(payload: AgentInput) -> dict[str, Any]:
    return engine.add_agent(payload.model_dump())


@router.get("/tasks")
async def list_tasks() -> list[dict[str, Any]]:
    return engine.list_tasks()


@router.post("/tasks")
async def create_task(payload: TaskInput) -> dict[str, Any]:
    return engine.create_task(payload.model_dump())


@router.post("/tasks/{task_id}/run")
async def run_task(task_id: str) -> dict[str, Any]:
    return engine.run_task(task_id)


@router.post("/manager/run")
async def manager_run() -> dict[str, Any]:
    return await run_manager_cycle()


@router.get("/notifications")
async def list_notifications() -> list[dict[str, Any]]:
    return engine.list_notifications()


@router.post("/command")
async def create_command(payload: dict[str, Any]) -> dict[str, Any]:
    task = engine.create_task({
        "title": payload.get("title") or payload.get("text") or "New company mission",
        "description": payload.get("description", ""),
        "task_type": payload.get("task_type", "general"),
        "priority": payload.get("priority", 5),
        "assignee": payload.get("assignee"),
    })
    engine.run_task(task["id"])
    return {"status": "queued", "task": task}


@router.get("/research")
async def get_research() -> list[dict[str, Any]]:
    return engine.list_research()


@router.post("/research")
async def do_research(payload: ResearchInput) -> dict[str, Any]:
    results = await search_web(payload.query, limit=5)
    engine.save_research(results)
    return {"query": payload.query, "results": results}


@router.post("/research/page")
async def read_research_page(payload: dict[str, Any]) -> dict[str, Any]:
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing url")
    return await read_page(url)


@router.get("/gmail/status")
async def gmail_status() -> dict[str, Any]:
    return engine.get_gmail()


@router.post("/gmail/config")
async def gmail_config(payload: GmailConfigInput) -> dict[str, Any]:
    config = {
        "status": "configured",
        "client_id": payload.client_id,
        "client_secret": payload.client_secret,
        "redirect_uri": payload.redirect_uri or "http://localhost:8000/api/gmail/callback",
    }
    engine.set_gmail(config)
    return config


@router.get("/gmail/start")
async def gmail_start() -> dict[str, Any]:
    return {"url": build_oauth_url()}


@router.get("/gmail/callback")
async def gmail_callback(code: str | None = None, state: str | None = None) -> dict[str, Any]:
    if not code:
        raise HTTPException(status_code=400, detail="Missing Google authorization code")
    result = await exchange_code(code, state)
    return result


@router.get("/gmail/messages")
async def gmail_messages() -> dict[str, Any]:
    return await list_gmail_messages()


@router.post("/gmail/send")
async def gmail_send(payload: dict[str, Any]) -> dict[str, Any]:
    to = payload.get("to")
    subject = payload.get("subject")
    body = payload.get("body")
    if not to or not subject or not body:
        raise HTTPException(status_code=400, detail="to, subject and body are required")
    return await send_gmail_message(to, subject, body)


@router.get("/files")
async def get_files() -> list[dict[str, Any]]:
    return engine.list_files()


@router.post("/files")
async def save_file(payload: dict[str, Any]) -> dict[str, Any]:
    return engine.save_file(payload)


@router.get("/resources")
async def get_resources() -> list[dict[str, Any]]:
    return engine.get_resources()


__all__ = ["router"]


path="backend/app/routes.py" 
