---
id: 8
title: list-todos-skill-spec
stage: general
date_iso: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: phase-3
user: WorkSpace
command: sp.specify Create a reusable intelligence skill specification named `list_todos.
labels:
  - skill
  - todo
  - specification
  - sdd
links:
  spec: skills/list_todos.skill.md
  ticket: null
  adr: null
  pr: null
files:
  - skills/list_todos.skill.md
tests: []
---

# Prompt

```
Create a reusable intelligence skill specification named `list_todos`.

Output format:
- File name: skills/list_todos.skill.md

Purpose:
- Retrieve todos for a user.

Inputs:
- user_id
- optional filters (status, priority)

Rules:
- Stateless
- Read-only
- Deterministic
```

# Response

Created a comprehensive skill specification for the list_todos reusable intelligence skill. The specification includes:

- Clear purpose statement defining the skill's role
- Detailed input parameter definitions with required/optional status
- Comprehensive behavior rules covering validation, processing, and output requirements
- Structured output formats for both success and error cases
- Implementation constraints that align with constitutional requirements
- Usage context explaining how the skill fits into the AI Agent ecosystem
- Dependencies listing required system components

The specification ensures the skill follows all required behavior rules: stateless operation, read-only access, deterministic output, ownership enforcement via user_id, proper input validation, structured output, and no external AI dependencies.

# Outcome

Successfully created a complete skill specification that meets all requirements and follows the constitutional principles for reusable intelligence skills.