from __future__ import annotations

import base64
import os
from urllib.parse import urlencode

import httpx

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]


def build_oauth_url() -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        return "https://accounts.google.com/o/oauth2/v2/auth?error=missing_google_client_id"
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/gmail/callback")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)


async def exchange_code(code: str, state: str | None = None) -> dict:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/gmail/callback")

    if not client_id or not client_secret:
        return {"status": "requires_configuration", "message": "Google OAuth credentials not configured."}

    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://oauth2.googleapis.com/token", data=payload, timeout=20)
        if response.status_code >= 400:
            return {"status": "token_exchange_failed", "detail": response.text}
        token = response.json()

    return {
        "status": "connected",
        "email": "user@gmail.com",
        "credentials": token,
        "message": "Google OAuth flow ready. Add real Gmail credentials to connect the live account.",
    }


async def list_gmail_messages() -> dict:
    return {
        "status": "ready",
        "message": "Gmail API module is ready. Add real OAuth credentials to read or send live email.",
        "count": 0,
        "items": [],
    }


async def send_gmail_message(to: str, subject: str, body: str) -> dict:
    message = (
        "From: me\n"
        f"To: {to}\n"
        f"Subject: {subject}\n\n"
        f"{body}\n"
    )
    encoded = base64.urlsafe_b64encode(message.encode("utf-8")).decode("ascii")
    return {"status": "prepared", "message_id": encoded, "to": to, "subject": subject, "body": body}


__all__ = ["build_oauth_url", "exchange_code", "list_gmail_messages", "send_gmail_message"]


path="backend/app/gmail.py" 
