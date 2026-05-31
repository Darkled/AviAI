---
story: STORY-002
prd: PRD-001
slug: postgres-connectivity
title: PostgreSQL Connectivity & Schema Service
type: NEW_CAPABILITY
complexity: SMALL
epic_branch: epic/PRD-001-ai-postgres-chat
created: 2026-05-31
---

# Plan: PostgreSQL Connectivity & Schema Service

## Summary

This plan covers establishing an asynchronous connection to PostgreSQL and implementing a service to retrieve the database schema. We will update the database core to use `sqlalchemy.ext.asyncio`, create a service that queries `information_schema` to discover tables and columns, and expose this information via a new API endpoint.

## User Story

As a developer, I want to establish a read-only connection to the PostgreSQL database and create a service to retrieve the database schema, so that the AI agent can understand the data structure.

## Story Reference

- Story file: `.agents/stories/PRD-001-ai-postgres-chat/STORY-002-postgres-connectivity.md`
- PRD: `.agents/PRDs/PRD-001-ai-postgres-chat/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | SMALL |
| Systems Affected | Backend (Core, Services, Routers) |
| Story | STORY-002 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-ai-postgres-chat` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Guidance on FastAPI async operations and RORO pattern. | Task 3, Task 4 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/app/routers/health.py
router = APIRouter()
@router.get("/health", response_model=HealthResponse)
```

### Async Database
We will use `sqlalchemy.ext.asyncio.create_async_engine` and `async_sessionmaker`.

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/database.py` | UPDATE | Switch to asynchronous SQLAlchemy engine and session. |
| `backend/app/schemas/schema.py` | CREATE | Define Pydantic models for database schema representation. |
| `backend/app/services/schema_service.py` | CREATE | Logic to query `information_schema` for tables and columns. |
| `backend/app/routers/schema.py` | CREATE | API endpoint to retrieve the database schema. |
| `backend/app/main.py` | UPDATE | Include the new schema router. |

---

## Tasks

### Task 1: Update Database Core to Async

- **File**: `backend/app/core/database.py`
- **Action**: UPDATE
- **Implement**: 
    - Use `create_async_engine` and `async_sessionmaker`.
    - Update `get_db` to be an async generator yielding an `AsyncSession`.
- **Mirror**: Standard SQLAlchemy 2.0 async patterns.
- **Validate**: `python -c "from app.core.database import engine; print('OK')"`

### Task 2: Create Schema Pydantic Models

- **File**: `backend/app/schemas/schema.py`
- **Action**: CREATE
- **Implement**: Define `ColumnSchema`, `TableSchema`, and `DatabaseSchema` models.
- **Mirror**: Follow existing schema patterns in `backend/app/schemas/`.
- **Validate**: N/A

### Task 3: Implement Schema Service

- **File**: `backend/app/services/schema_service.py`
- **Action**: CREATE
- **Implement**: 
    - Function `get_database_schema(db: AsyncSession)` that queries `information_schema.tables` and `information_schema.columns`.
    - Return a `DatabaseSchema` object.
- **Mirror**: Functional service pattern.
- **Validate**: N/A

### Task 4: Implement Schema Router

- **File**: `backend/app/routers/schema.py`
- **Action**: CREATE
- **Implement**: `GET /schema` endpoint that calls `schema_service.get_database_schema`.
- **Mirror**: `backend/app/routers/health.py`
- **Validate**: `GET /api/schema` returns valid JSON.

### Task 5: Register Schema Router

- **File**: `backend/app/main.py`
- **Action**: UPDATE
- **Implement**: Include `schema.router` with prefix `/api`.
- **Mirror**: Health router registration.
- **Validate**: Server starts without error.

---

## End-to-End Tests

- [ ] Start backend.
- [ ] Hit `GET /api/schema` → returns list of tables (e.g., `aircraft_models`, `fleet`) and their columns.
- [ ] Verify data types and nullability are correctly captured.

---

## Validation

```bash
cd backend
python -m pytest tests/test_health.py # Ensure no regression
curl http://localhost:8000/api/schema
```

---

## Acceptance Criteria

- [x] Given a valid `DATABASE_URL`, when the backend starts, then it successfully connects to PostgreSQL using `asyncpg`.
- [x] Given a connected database, when I call the schema service, then it returns a structured representation of the tables and columns.
- [x] Given a `GET /api/schema` request, when authorized, then it returns the current database schema in JSON format.
- [ ] All tasks completed
- [ ] Backend server starts without error
- [ ] Follows existing patterns
