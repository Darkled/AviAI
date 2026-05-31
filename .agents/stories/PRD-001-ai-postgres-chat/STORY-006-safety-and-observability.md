---
id: STORY-006
prd: PRD-001
slug: safety-and-observability
title: SQL Safety & Observability
type: technical
priority: medium
complexity: small
phase: 4
status: todo
labels: [backend, security, logging]
epic_branch: epic/PRD-001-ai-postgres-chat
plan: null
report: null
commit: null
depends_on: [STORY-004, STORY-005]
blocks: []
skills: [building-pydantic-ai-agents]
created: 2026-05-31
updated: 2026-05-31
---

# STORY-006: SQL Safety & Observability

## Description

As an administrator, I want to ensure all AI-generated queries are safe and all agent activities are logged, so that I can monitor and secure the system.

## Acceptance Criteria

- [ ] Given any AI-generated SQL, when before execution, then it is validated against a blacklist of destructive commands (DROP, TRUNCATE, etc.).
- [ ] Given an agent run, when completed, then a full trace is visible in Logfire including model inputs, tool calls, and outputs.
- [ ] Given a query error, when it occurs, then the error is logged and a user-friendly message is displayed.

## Technical Notes

- Implement SQL validation in `backend/app/services/ai_service.py` or a dedicated middleware.
- Ensure `logfire.instrument_pydantic_ai()` is correctly configured.
- Use `logfire.instrument_httpx(capture_all=True)` for deep visibility.

## Dependencies

- **Blocked by**: STORY-004, STORY-005
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-ai-postgres-chat/PRD.md) — Implementation Phases: Phase 4
