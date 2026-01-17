---
id: 5
title: create-todo-skill-spec
stage: general
date_iso: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: phase-3
user: WorkSpace
command: sp.specify Create a reusable intelligence skill specification named `create_todo.
labels:
  - skill
  - todo
  - specification
  - sdd
links:
  spec: skills/create_todo.skill.md
  ticket: null
  adr: null
  pr: null
files:
  - skills/create_todo.skill.md
tests: []
---

# Prompt

```
Create a reusable intelligence skill specification named `create_todo`.

Output format:
- File name: skills/create_todo.skill.md

Purpose:
- Create a new todo item for an authenticated user.

Inputs:
- user_id (string, provided by agent)
- title (string, required)
- description (string, optional)
- priority (low | medium | high, optional)
- due_date (ISO string, optional)

Behavior rules:
- Skill must be stateless and deterministic
- No authentication or authorization logic
- No HTTP or UI logic
- Must validate input shape
- Must return structured output (success or error)
- Must not assume external AI or LLM availability

Usage:
- This skill will be invoked only by an AI Agent.
```

# Response

Created a comprehensive skill specification for the create_todo reusable intelligence skill. The specification includes:

- Clear purpose statement defining the skill's role
- Detailed input parameter definitions with required/optional status
- Comprehensive behavior rules covering validation, processing, and output requirements
- Structured output formats for both success and error cases
- Implementation constraints that align with constitutional requirements
- Usage context explaining how the skill fits into the AI Agent ecosystem
- Dependencies listing required system components

The specification ensures the skill follows all required behavior rules: stateless operation, deterministic output, no authentication/authorization logic, proper input validation, structured output, and no external AI dependencies.

# Outcome

Successfully created a complete skill specification that meets all requirements and follows the constitutional principles for reusable intelligence skills.