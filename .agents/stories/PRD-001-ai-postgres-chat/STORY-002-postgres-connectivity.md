---
id: STORY-002
prd: PRD-001
slug: postgres-connectivity
title: PostgreSQL Connectivity & Schema Service
type: technical
priority: high
complexity: small
phase: 1
status: done
labels: [backend, postgres]
epic_branch: epic/PRD-001-ai-postgres-chat
plan: .agents/plans/PRD-001-ai-postgres-chat/completed/STORY-002-postgres-connectivity.plan.md
report: .agents/reports/PRD-001-ai-postgres-chat/STORY-002-postgres-connectivity.report.md
commit: 45df6b9
depends_on: [STORY-001]
blocks: [STORY-004]
skills: [fastapi-python]
created: 2026-05-31
updated: 2026-05-31
---

# STORY-002: PostgreSQL Connectivity & Schema Service

## Description

As a developer, I want to establish a read-only connection to the PostgreSQL database and create a service to retrieve the database schema, so that the AI agent can understand the data structure.

## Acceptance Criteria

- [ ] Given a valid `DATABASE_URL`, when the backend starts, then it successfully connects to PostgreSQL using `asyncpg`.
- [ ] Given a connected database, when I call the schema service, then it returns a structured representation of the tables and columns.
- [ ] Given a `GET /api/schema` request, when authorized, then it returns the current database schema in JSON format.

## Technical Notes

- Use `asyncpg` for asynchronous database interaction in `backend/app/core/database.py`.
- Implement a service in `backend/app/services/schema_service.py` to query `information_schema`.
- Ensure the connection is strictly read-only as per PRD Security & Configuration.

## Dependencies

- **Blocked by**: STORY-001
- **Blocks**: STORY-004

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-ai-postgres-chat/PRD.md) — Implementation Phases: Phase 1 & 2
