---
id: 6
title: update-todo-skill-spec
stage: general
date_iso: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: phase-3
user: WorkSpace
command: sp.specify Create a reusable intelligence skill specification named `update_todo.
labels:
  - skill
  - todo
  - specification
  - sdd
links:
  spec: skills/update_todo.skill.md
  ticket: null
  adr: null
  pr: null
files:
  - skills/update_todo.skill.md
tests: []
---

# Prompt

```
Create a reusable intelligence skill specification named `update_todo`.

Output format:
- File name: skills/update_todo.skill.md

Purpose:
- Update an existing todo item.

Inputs:
- user_id
- todo_id
- updated fields (title, description, priority, due_date, completed)

Rules:
- Stateless
- Deterministic
- Ownership enforced via user_id
- No auth, UI, or HTTP logic
```

# Response

Created a comprehensive skill specification for the update_todo reusable intelligence skill. The specification includes:

- Clear purpose statement defining the skill's role
- Detailed input parameter definitions with required/optional status
- Comprehensive behavior rules covering validation, processing, and output requirements
- Structured output formats for both success and error cases
- Implementation constraints that align with constitutional requirements
- Usage context explaining how the skill fits into the AI Agent ecosystem
- Dependencies listing required system components

The specification ensures the skill follows all required behavior rules: stateless operation, deterministic output, ownership enforcement via user_id, proper input validation, structured output, and no external AI dependencies.

# Outcome

Successfully created a complete skill specification that meets all requirements and follows the constitutional principles for reusable intelligence skills.