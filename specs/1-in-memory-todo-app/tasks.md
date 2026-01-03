# Tasks: In-Memory Python Console Todo App (Phase I)

**Input**: Design documents from `/specs/1-in-memory-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Phase 1: Setup

**Purpose**: Project initialization and basic structure.

- [X] T001 Initialize Python project using `uv`: `uv init`
- [X] T002 [P] Create the source code directory structure: `src/todo/`
- [X] T003 [P] Create placeholder files: `src/todo/__init__.py`, `src/todo/main.py`, `src/todo/engine.py`, `src/todo/models.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model that all user stories depend on.

- [X] T004 Define the `Todo` data class in `src/todo/models.py` with attributes: `id: int`, `title: str`, `is_completed: bool`, `created_at: datetime`.

---

## Phase 3: User Story 1 - Add a new task (Priority: P1) 🎯 MVP

**Goal**: Allow a user to add a new task to the in-memory list.
**Independent Test**: Verify that a new task can be added and appears in the task list.

### Implementation for User Story 1

- [X] T005 [US1] Implement the `TodoManager` class in `src/todo/engine.py` with an in-memory list for tasks.
- [X] T006 [US1] Implement the `add_task(title: str)` method in the `TodoManager` class.
- [X] T007 [US1] Set up the main REPL loop in `src/todo/main.py`.
- [X] T008 [US1] Add a `match-case` block to handle the `add` command in `src/todo/main.py`.

---

## Phase 4: User Story 2 - View all tasks (Priority: P1)

**Goal**: Allow a user to view all tasks.
**Independent Test**: Verify that all added tasks are displayed with their correct status.

### Implementation for User Story 2

- [X] T009 [US2] Implement the `list_tasks()` method in the `TodoManager` class in `src/todo/engine.py`.
- [X] T010 [US2] Implement the `view` command in `src/todo/main.py` to display tasks.

---

## Phase 5: User Story 3 - Mark a task as complete (Priority: P1)

**Goal**: Allow a user to mark a task as complete.
**Independent Test**: Verify that a task's status can be updated to "Complete".

### Implementation for User Story 3

- [X] T011 [US3] Implement the `mark_complete(task_id: int)` method in `src/todo/engine.py`.
- [X] T012 [US3] Add the `done` command to `src/todo/main.py` to mark tasks as complete.
- [X] T013 [US3] Add error handling in `src/todo/main.py` for non-existent task IDs.

---

## Phase 6: User Story 4 - Delete a task (Priority: P2)

**Goal**: Allow a user to delete a task.
**Independent Test**: Verify that a task can be removed from the list.

### Implementation for User Story 4

- [X] T014 [US4] Implement the `delete_task(task_id: int)` method in `src/todo/engine.py`.
- [X] T015 [US4] Add the `del` command to `src/todo/main.py` to delete tasks.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation.

- [ ] T016 [P] Add Google-style docstrings to all functions and classes.
- [ ] T017 Refine CLI output formatting for clarity in `src/todo/main.py`.
- [X] T018 Implement a `help` command in `src/todo/main.py` to show available commands.
- [ ] T019 Update `README.md` with instructions on how to run and use the application.

---

## Dependencies & Execution Order

- **Phase 1 & 2**: Must be completed first.
- **User Stories**: Can be implemented in priority order (P1 then P2). US1, US2, and US3 are all P1 and can be worked on in any order after Phase 2 is complete. US4 is P2 and should be done after the P1 stories.
- **Polish**: Should be done last.
