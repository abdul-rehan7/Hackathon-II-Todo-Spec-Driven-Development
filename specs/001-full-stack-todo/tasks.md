# Tasks: Phase II Full-Stack Todo App Evolution

**Input**: Design documents from `/specs/001-full-stack-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Tests are included as requested by the plan and spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below adjust based on `plan.md` structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure in `backend/` and frontend project structure in `frontend/`
- [x] T002 Initialize Python project for backend with FastAPI and SQLModel in `backend/`
- [x] T003 Initialize Next.js project for frontend in `frontend/`
- [x] T004 [P] Configure linting and formatting tools for backend (e.g., Black, Flake8) in `backend/`
- [x] T005 [P] Configure linting and formatting tools for frontend (e.g., ESLint, Prettier) in `frontend/`
- [x] T006 Create `.env` file in `backend/` and `frontend/` for environment variables, including `DATABASE_URL`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Setup database connection and session management in `backend/src/database/`
- [x] T008 Generate SQLModel `Todo` database models in `backend/src/models/todo.py`
- [x] T009 Configure database migration framework for Neon DB in `backend/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Manage Todos (Priority: P1) 🎯 MVP

**Goal**: Implement full CRUD functionality for Todo items via web UI.

**Independent Test**: User can interact with the web UI to perform all CRUD operations on todo items, and verify changes are reflected and persisted.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Unit test `Todo` model validation in `backend/tests/unit/test_todo_model.py`
- [ ] T011 [P] [US1] Integration test for backend `Todo` creation in `backend/tests/integration/test_todo_api.py`
- [ ] T012 [P] [US1] Integration test for backend `Todo` listing in `backend/tests/integration/test_todo_api.py`
- [ ] T013 [P] [US1] Integration test for backend `Todo` update in `backend/tests/integration/test_todo_api.py`
- [ ] T014 [P] [US1] Integration test for backend `Todo` deletion in `backend/tests/integration/test_todo_api.py`
- [ ] T015 [P] [US1] Unit test for frontend `AddTodo` component in `frontend/tests/unit/add_todo.test.tsx`
- [ ] T016 [P] [US1] Unit test for frontend `TodoList` component in `frontend/tests/unit/todo_list.test.tsx`

### Implementation for User Story 1

- [X] T017 [US1] Implement FastAPI CRUD endpoints for `Todo` in `backend/src/api/v1/endpoints/todos.py`
- [X] T018 [US1] Add validation and error handling for `Todo` APIs in `backend/src/api/v1/endpoints/todos.py`
- [X] T019 [P] [US1] Create Next.js `AddTodo` page/component in `frontend/src/app/todos/add/page.tsx` or `frontend/src/components/AddTodo.tsx`
- [X] T020 [P] [US1] Create Next.js `TodoList` page/component in `frontend/src/app/todos/page.tsx` or `frontend/src/components/TodoList.tsx`
- [X] T021 [P] [US1] Create Next.js `UpdateTodo` page/component in `frontend/src/app/todos/[id]/edit/page.tsx` or `frontend/src/components/UpdateTodo.tsx`
- [X] T022 [P] [US1] Create Next.js `DeleteTodo` functionality (e.g., as part of `TodoList` or a dedicated component)
- [X] T023 [US1] Connect frontend `AddTodo` to backend API in `frontend/src/services/todoService.ts`
- [X] T024 [US1] Connect frontend `TodoList` to backend API in `frontend/src/services/todoService.ts`
- [X] T025 [US1] Connect frontend `UpdateTodo` to backend API in `frontend/src/services/todoService.ts`
- [X] T026 [US1] Connect frontend `DeleteTodo` to backend API in `frontend/src/services/todoService.ts`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 Run local end-to-end testing to verify all functionality (UI to DB interaction)
- [ ] T028 Refine `specs/001-full-stack-todo/spec.md` or `specs/001-full-stack-todo/plan.md` if Claude output fails or errors occur during implementation
- [ ] T029 Commit all generated and implemented code to the `phase-2` branch
- [ ] T030 Tag the milestone as "Phase II Complete" for eventual merge into `main`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Polish (Final Phase)**: Depends on User Story 1 completion

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services/APIs
- Backend APIs before frontend components
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T004, T005, T006)
- All Foundational tasks marked [P] can run in parallel (N/A in this specific case)
- Once Foundational phase completes, User Story 1 tests marked [P] can run in parallel (T010-T016)
- User Story 1 frontend components creation tasks marked [P] can run in parallel (T019-T022)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run independent tests for User Story 1, perform manual UI testing.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
