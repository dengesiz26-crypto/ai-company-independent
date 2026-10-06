# AI Company OS

A production-ready structure for a mobile-friendly AI operations company app with:
- AI company dashboard
- 10 specialized agent roles
- task orchestration and manager routing
- Gmail OAuth integration
- research tooling
- file system and sandbox access
- user-controlled connections
- Expo mobile frontend and FastAPI backend

This repository is intentionally independent of Emergent services. It uses standard Python and modern web tooling.

## Stack
- Backend: FastAPI + Pydantic + Google API + optional OpenAI support
- Frontend: Expo React Native + Expo Router
- Storage: JSON file persistence for local development

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npx expo start
```

Then open the app in Expo Go or browser.

## Default routes

- Backend: http://localhost:8000
- API: http://localhost:8000/api
- Health: http://localhost:8000/api/health
- Dashboard: http://localhost:8000/api/dashboard
- Agents: http://localhost:8000/api/agents
- Tasks: http://localhost:8000/api/tasks
- Gmail: http://localhost:8000/api/gmail/status

## Note about Gmail

Gmail OAuth requires Google Cloud OAuth credentials. The app is built to work with a real Google OAuth flow, but it will remain functional even without credentials by returning configuration guidance.

## Important

This is a real, code-based foundation for the system you described. It is designed to run locally and extend easily.
