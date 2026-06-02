---
id: STORY-004
prd: PRD-001
slug: ai-agent-implementation
title: Pydantic AI Agent Implementation
type: feature
priority: high
complexity: medium
phase: 2
status: done
labels: [backend, ai, pydantic-ai]
epic_branch: epic/PRD-001-ai-postgres-chat
plan: .agents/plans/story-004-ai-agent-implementation.md
report: null
commit: null
depends_on: [STORY-002]
blocks: [STORY-005, STORY-006]
skills: [building-pydantic-ai-agents]
created: 2026-05-31
updated: 2026-06-02
---

# STORY-004: Pydantic AI Agent Implementation

## Description

As a user, I want to ask questions in natural language, so that the AI agent can translate my intent into SQL and retrieve the relevant data.

## Acceptance Criteria

- [x] Given a natural language query, when the agent runs, then it correctly identifies the required SQL query.
- [x] Given a generated SQL query, when the agent executes it, then it returns the raw data from the database.
- [x] Given the data, when the agent responds, then it provides a human-readable explanation of the results.
- [x] Given an invalid or dangerous query (e.g., DELETE), when the agent is asked, then it refuses to execute and explains why.

## Technical Notes

- Define the agent in `backend/app/services/ai_service.py` using `pydantic_ai`.
- Configure OpenRouter as the provider.
- Implement tools: `execute_sql` (read-only) and `get_schema`.
- Use Logfire for tracing and debugging.

## Dependencies

- **Blocked by**: STORY-002
- **Blocks**: STORY-005, STORY-006

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-ai-postgres-chat/PRD.md) — Implementation Phases: Phase 2
