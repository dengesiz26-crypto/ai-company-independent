from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.engine import engine
from app.schemas import AgentInput, CompanyInput, GmailConfigInput, ResearchInput, TaskInput
from app.gmail import build_oauth_url, exchange_code, list_gmail_messages, send_gmail_message
from app.research import search_web, read_page

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, Any]:
    return {"ok": True, "service": "AICorpOS"}


@router.get("/dashboard")
async def dashboard() -> dict[str, Any]:
    return engine.dashboard()


@router.get("/company")
async def get_company() -> dict[str, Any]:
    return engine.ensure_seed()


@router.post("/company")
async def create_company(payload: CompanyInput) -> dict[str, Any]:
    return engine.create_or_update_company(payload.model_dump(exclude_none=True))


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
    task = engine.create_task(payload.model_dump())
    return task


@router.post("/tasks/{task_id}/run")
async def run_task(task_id: str) -> dict[str, Any]:
    return engine.run_task(task_id)


@router.get("/notifications")
async def list_notifications() -> list[dict[str, Any]]:
    return engine.list_notifications()


@router.post("/command")
async def create_command(payload: dict[str, Any]) -> dict[str, Any]:
    title = payload.get("title") or payload.get("text") or "New company mission"
    task_type = payload.get("task_type") or "general"
    task = engine.create_task({
        "title": title,
        "description": payload.get("description", ""),
        "task_type": task_type,
        "priority": payload.get("priority", 5),
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
async def fetch_page(payload: dict[str, Any]) -> dict[str, Any]:
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
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
    url = build_oauth_url()
    return {"url": url}


@router.get("/gmail/callback")
async def gmail_callback(code: str | None = None, state: str | None = None) -> dict[str, Any]:
    if not code:
        raise HTTPException(status_code=400, detail="Google code is missing")
    result = await exchange_code(code, state)
    engine.set_gmail({"status": "connected", "email": result.get("email"), "credentials": result.get("credentials")})
    return {"ok": True, "message": "Google account connected", "email": result.get("email")}


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
    return await send_gmail_message(to=to, subject=subject, body=body)


@router.get("/files")
async def list_files() -> list[dict[str, Any]]:
    return engine.store.load("files", [])


@router.post("/files")
async def save_file(payload: dict[str, Any]) -> dict[str, Any]:
    items = engine.store.load("files", [])
    entry = {
        "id": payload.get("id") or f"file-{len(items)+1}",
        "name": payload["name"],
        "path": payload.get("path", "/tmp"),
        "content": payload.get("content", ""),
        "updated_at": __import__("datetime").datetime.utcnow().isoformat(),
    }
    items.append(entry)
    engine.store.save("files", items)
    return entry
