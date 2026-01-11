---
description: "Task list for user authentication implementation"
---

# Tasks: User Authentication

**Input**: Design documents from `/specs/1-user-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Install better-auth.com and related dependencies in frontend/package.json
- [x] T002 [P] Install better-auth.com and related dependencies in backend/requirements.txt
- [x] T003 Create .env files for auth configuration in root directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create User model in backend/src/models/user.py
- [x] T005 [P] Create migration script for User table in backend/migrations/
- [x] T006 [P] Update Todo model to include user_id foreign key in backend/src/models/todo.py
- [x] T007 [P] Create migration script to add user_id to Todo table in backend/migrations/
- [x] T008 Configure better-auth SDK in backend/src/auth/config.py
- [x] T009 Create auth middleware to protect API endpoints in backend/src/middleware/auth_middleware.py
- [x] T010 [P] Create auth service layer in backend/src/services/auth_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: New users can create an account with email and password to access the Todo application.

**Independent Test**: New users can successfully register with valid email and password, receive confirmation of account creation, and be logged in to access their Todo list.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Contract test for registration endpoint in backend/tests/contract/test_auth.py
- [x] T012 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_registration.py
- [x] T013 [P] [US1] Frontend unit test for SignupForm component in frontend/tests/components/auth/signup.test.js

### Implementation for User Story 1

- [x] T014 [P] [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.jsx
- [x] T015 [P] [US1] Create signup page in frontend/src/pages/signup.jsx
- [x] T016 [US1] Create signup API endpoint in backend/src/api/auth.py
- [x] T017 [US1] Add signup functionality to auth service in backend/src/services/auth_service.py
- [x] T018 [US1] Add validation for email format and password strength in backend/src/utils/validation.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Registered users can log in with their credentials to access their personal Todo data.

**Independent Test**: Returning users can authenticate with valid credentials and gain access to their personal Todo items with proper session management.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T019 [P] [US2] Contract test for login endpoint in backend/tests/contract/test_auth.py
- [x] T020 [P] [US2] Integration test for user login flow in backend/tests/integration/test_login.py
- [x] T021 [P] [US2] Frontend unit test for LoginForm component in frontend/tests/components/auth/login.test.js

### Implementation for User Story 2

- [x] T022 [P] [US2] Create LoginForm component in frontend/src/components/auth/LoginForm.jsx
- [x] T023 [P] [US2] Create login page in frontend/src/pages/login.jsx
- [x] T024 [US2] Create login API endpoint in backend/src/api/auth.py
- [x] T025 [US2] Add login functionality to auth service in backend/src/services/auth_service.py
- [x] T026 [US2] Implement session handling in frontend/src/services/authService.js

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Todo Access (Priority: P1)

**Goal**: Authenticated users can only see their own Todo items, and unauthenticated users are redirected to login.

**Independent Test**: Users can only view, create, update, and delete their own Todo items, with unauthorized access attempts redirecting to login page.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T027 [P] [US3] Contract test for protected Todo endpoints in backend/tests/contract/test_todos.py
- [x] T028 [P] [US3] Integration test for user-scoped Todo access in backend/tests/integration/test_todo_scoping.py
- [x] T029 [P] [US3] Frontend unit test for ProtectedRoute component in frontend/tests/components/auth/protectedRoute.test.js

### Implementation for User Story 3

- [x] T030 [P] [US3] Create ProtectedRoute component in frontend/src/components/auth/ProtectedRoute.jsx
- [x] T031 [US3] Update Todo API endpoints to enforce user scoping in backend/src/api/todos.py
- [x] T032 [US3] Update Todo service to filter by authenticated user in backend/src/services/todo_service.py
- [x] T033 [US3] Update frontend Todo service to include auth headers in frontend/src/services/todoService.js
- [x] T034 [US3] Add redirect logic for unauthenticated access in frontend/src/utils/routeGuard.js

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - User Logout (Priority: P2)

**Goal**: Users can securely log out of their session, clearing authentication state.

**Independent Test**: Users can terminate their session, clear authentication tokens, and be redirected to public landing page.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T035 [P] [US4] Contract test for logout endpoint in backend/tests/contract/test_auth.py
- [x] T036 [P] [US4] Integration test for user logout flow in backend/tests/integration/test_logout.py

### Implementation for User Story 4

- [x] T037 [P] [US4] Create logout API endpoint in backend/src/api/auth.py
- [x] T038 [US4] Add logout functionality to auth service in backend/src/services/auth_service.py
- [x] T039 [US4] Add logout handler to frontend auth service in frontend/src/services/authService.js
- [x] T040 [US4] Create logout button component in frontend/src/components/auth/LogoutButton.jsx

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T041 [P] Update existing Todo API calls to require authentication in backend/src/api/todos.py
- [x] T042 [P] Add comprehensive error handling for auth failures in frontend/src/utils/errorHandler.js
- [x] T043 Add security headers and validation in backend/src/middleware/security.py
- [x] T044 [P] Update documentation in docs/authentication.md
- [x] T045 Add integration tests for complete auth + Todo workflow in backend/tests/e2e/test_auth_flow.py
- [x] T046 Run quickstart.md validation to ensure all components work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on auth foundation

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for registration endpoint in backend/tests/contract/test_auth.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_registration.py"
Task: "Frontend unit test for SignupForm component in frontend/tests/components/auth/signup.test.js"

# Launch all implementation tasks for User Story 1 together:
Task: "Create SignupForm component in frontend/src/components/auth/SignupForm.jsx"
Task: "Create signup page in frontend/src/pages/signup.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence