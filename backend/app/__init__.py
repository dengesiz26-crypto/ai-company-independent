# AI Company OS

This repository is a real, mobile-friendly AI-company operating system foundation designed to be independent from Emergent services.

## Included
- 10 specialized agent roles
- Executive manager + task routing
- Gmail OAuth-ready integration
- Research module with external resource links
- File storage and task persistence
- FastAPI backend with JSON persistence
- Expo mobile frontend dashboard for agents, tasks, Gmail, and company operations

## Run locally

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

## Key endpoints
- GET /api/health
- GET /api/dashboard
- GET /api/company
- GET /api/agents
- GET /api/tasks
- GET /api/research
- GET /api/gmail/status
- POST /api/command
- POST /api/tasks
- POST /api/tasks/{id}/run

## Notes
- Gmail OAuth needs real Google Cloud credentials.
- The app is structured to be production-ready as a local foundation.
- This repo intentionally avoids Emergent-only dependencies.


path="README.md" 
