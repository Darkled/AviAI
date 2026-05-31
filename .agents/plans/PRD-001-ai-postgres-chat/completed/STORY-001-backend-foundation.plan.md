---
story: STORY-001
prd: PRD-001
slug: backend-foundation
title: Backend Foundation & API Skeleton
type: NEW_CAPABILITY
complexity: LOW
epic_branch: epic/PRD-001-ai-postgres-chat
created: 2026-05-31
---

# Plan: Backend Foundation & API Skeleton

## Summary

This plan covers the initial setup of the FastAPI backend for the AI PostgreSQL Chat Agent. We will reorganize the existing boilerplate to follow a modular router-based structure, define proper schemas for basic API responses, and ensure all necessary dependencies (Pydantic AI, asyncpg, Logfire) are present in `requirements.txt`.

## User Story

As a developer, I want to set up the FastAPI project structure and a basic health check endpoint, so that I have a solid foundation for the application.

## Story Reference

- Story file: `.agents/stories/PRD-001-ai-postgres-chat/STORY-001-backend-foundation.md`
- PRD: `.agents/PRDs/PRD-001-ai-postgres-chat/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | LOW |
| Systems Affected | Backend (FastAPI, requirements) |
| Story | STORY-001 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-ai-postgres-chat` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Guidance on FastAPI structure, functional components, and Pydantic models. | Task 2, Task 3, Task 4 |
| building-pydantic-ai-agents | Ensuring initial dependencies for Pydantic AI and Logfire are included. | Task 1 |

---

## Patterns to Follow

### Naming
```python
# SOURCE: backend/app/core/config.py
class Settings(BaseSettings):
    app_name: str = "FastAPI Template"
```

### Error Handling
FastAPI's built-in `HTTPException` will be used for standard error responses, following the `fastapi-python` skill's guidance on functional components.

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/requirements.txt` | UPDATE | Add Pydantic AI, asyncpg, and Logfire dependencies. |
| `backend/app/schemas/health.py` | CREATE | Define the Pydantic model for the health check response. |
| `backend/app/routers/health.py` | CREATE | Move health check logic to a dedicated router. |
| `backend/app/main.py` | UPDATE | Refactor to use the health router and update app metadata. |
| `backend/app/core/config.py` | UPDATE | Add settings for OpenRouter and Logfire. |

---

## Tasks

### Task 1: Update Dependencies

- **File**: `backend/requirements.txt`
- **Action**: UPDATE
- **Implement**: Add `pydantic-ai`, `asyncpg`, `logfire`, and `httpx` to the list of requirements.
- **Validate**: `pip install -r backend/requirements.txt` (dry run or check syntax).

### Task 2: Create Health Schema

- **File**: `backend/app/schemas/health.py`
- **Action**: CREATE
- **Implement**: Define a `HealthResponse` Pydantic model with `status: str` and `version: str`.
- **Mirror**: Follow `fastapi-python` guidance on using Pydantic models for validation.
- **Validate**: N/A (Internal model definition).

### Task 3: Implement Health Router

- **File**: `backend/app/routers/health.py`
- **Action**: CREATE
- **Implement**: Create an `APIRouter` and define the `GET /health` endpoint using the `HealthResponse` schema.
- **Mirror**: Follow modular router pattern mentioned in `fastapi-python` skill.
- **Validate**: N/A (Unit testable later).

### Task 4: Refactor Main Application

- **File**: `backend/app/main.py`
- **Action**: UPDATE
- **Implement**: 
    - Remove the inline `/health` endpoint.
    - Include the `health` router with prefix `/api`.
    - Update the `FastAPI` app title to "AI PostgreSQL Chat API".
- **Validate**: `cd backend && python -m uvicorn app.main:app --reload` (server starts and `/api/health` returns 200).

### Task 5: Update Configuration

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Add `openrouter_api_key`, `openrouter_model`, and `logfire_token` fields to the `Settings` class.
- **Validate**: Check if settings load correctly from `.env`.

---

## End-to-End Tests

- [ ] Start backend: `cd backend && python -m uvicorn app.main:app`
- [ ] Hit `GET /api/health` → returns `{"status": "ok", "version": "0.1.0"}`
- [ ] Verify logs show the server starting with the new title.

---

## Validation

```bash
cd backend
python -m uvicorn app.main:app --reload
curl http://localhost:8000/api/health
```

---

## Acceptance Criteria

- [x] Given a running environment, when I start the backend, then the FastAPI server initializes without errors.
- [x] Given the backend is running, when I call `GET /api/health`, then I receive a `200 OK` response with a JSON body indicating status "ok".
- [x] Given the project structure, when I inspect the directories, then they align with the PRD (routers, services, models, core).
- [ ] All tasks completed
- [ ] Backend server starts without error
- [ ] Follows existing patterns
