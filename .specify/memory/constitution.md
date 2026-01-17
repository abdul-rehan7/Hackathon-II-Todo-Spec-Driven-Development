<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0
- List of modified principles:
  - No AI Features in Phase II (removed)
  - Phase III (AI Integration) (updated description to reflect new architecture)
- Added sections:
  - AI Agent Layer Integration
  - Reusable Intelligence via Skills
  - Stateless and Deterministic Skills
  - Separation of Concerns for Skills
  - AI Agent Responsibilities
  - No External LLM Dependency
  - Frontend Chat UI Implementation
  - Architecture Preservation
- Removed sections:
  - No AI Features in Phase II
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
  - ✅ .specify/templates/commands/sp.constitution.md
  - ✅ .specify/templates/commands/sp.phr.md
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Needs to be provided
-->
# Evolutionary AI-Powered Todo Ecosystem (Phase I to Phase V) Constitution

## Core Principles

### Architectural Foresight
Phase II code MUST be written with subsequent phases in mind to minimize future refactoring and ensure seamless evolution towards a full-stack, distributed system.

### Spec-Driven Development (SDD)
All code generation MUST be driven by detailed specifications. Manual coding is prohibited. Claude MUST generate all code from the provided specs, ensuring consistency and adherence to architectural guidelines.

### Branch-Based Development
All Phase II development work MUST be conducted on the `phase-2` branch. Merges into the `main` branch are permitted ONLY after successful validation and adherence to defined quality gates.

### Modular Decoupling
Maintain a strict separation between the frontend, backend business logic, and data storage layers to promote independent development, testing, and deployment.

### Production Readiness
Even in early phases, "Twelve-Factor App" methodologies MUST be followed to simplify the transition to containerized and cloud-native environments.

### Defined Tech Stack (Phase II)
The technology stack for Phase II MUST consist of Next.js for the frontend, FastAPI for the backend, and SQLModel with Neon DB (PostgreSQL) for data persistence. No alternative technologies are permitted without explicit architectural review.

### AI Agent Layer Integration
The system introduces an AI Agent layer for conversational interaction. This agent MUST serve as the intermediary between user input and business logic execution, enabling natural language interfaces to application functionality.

### Reusable Intelligence via Skills
Business logic MUST be implemented as reusable intelligence via skill.md files. Each skill represents a discrete, testable unit of business capability that can be orchestrated by the AI agent without duplication of logic across the codebase.

### Stateless and Deterministic Skills
Skills MUST be stateless, deterministic, and reusable. Each skill execution MUST produce consistent outputs for identical inputs without relying on external mutable state, ensuring predictability and testability across all interactions.

### Separation of Concerns for Skills
Skills MUST NOT handle authentication, authorization, HTTP, or UI logic. These cross-cutting concerns remain the responsibility of dedicated infrastructure layers, allowing skills to focus exclusively on pure business logic implementation.

### AI Agent Responsibilities
The AI Agent is responsible for intent detection, validation, user context injection, and skill orchestration. The agent MUST interpret user input, validate required context, inject user-specific data, and coordinate the execution of appropriate skills to fulfill user requests.

### No External LLM Dependency
No external LLM or OpenAI API keys are required; agent reasoning can be rule-based or mocked. The system architecture MUST support deterministic, locally-executable reasoning that does not rely on external services for core functionality, ensuring reliability and control over the AI interaction layer.

### Frontend Chat UI Implementation
Frontend chat UI MUST be implemented using Next.js components, not ChatKit. The conversational interface MUST leverage native Next.js capabilities and libraries rather than external chat frameworks to maintain consistency with the established tech stack and avoid additional dependencies.

### Architecture Preservation
Existing Phase 2 architecture (auth, DB, APIs) MUST remain unchanged. The AI Agent layer integrates as an additional layer without modifying the established authentication, database, or API structures, preserving the integrity of the existing system while extending functionality through the new conversational interface.

## Key Standards

- **Code Quality:** Strict adherence to PEP 8 for Python; utilize Type Hints for all function signatures to support SQLModel. Frontend code MUST follow established Next.js and TypeScript best practices.
- **Documentation:** Every significant function/component MUST have clear docstrings/comments; maintain a CHANGELOG.md to track progression through phases.
- **API Contracts:** All API endpoints MUST be well-defined with clear input/output schemas and error taxonomies.
- **Deployment Readiness:** Use environment variables for configuration to ensure seamless Dockerization and deployment.

## Phase-Specific Tech Stack Constraints

- **Phase I (Console App):** Python 3.11+, Claude Code for development, Spec-Kit Plus for testing/spec validation. Data stored in volatile memory (Lists/Dicts).
- **Phase II (Full-Stack Web App):** Next.js (Frontend), FastAPI (Backend), SQLModel with Neon DB (PostgreSQL).
- **Phase III (AI Integration):** Integration of AI Agent layer with skill.md files for business logic, rule-based reasoning engine, and Next.js chat UI components. No external LLM dependencies required. Existing Phase 2 architecture remains unchanged.
- **Phase IV (Containerization):** Containerization via Docker; orchestration using Minikube/Helm with kubectl-ai for cluster management. (Out of scope for current work)
- **Phase V (Distributed System):** Evolution to a distributed system using Kafka (event-driven) and Dapr (sidecars) on DigitalOcean DOKS. (Out of scope for current work)

## Governance

- **Success Criteria (Phase III Focus):**
  - AI Agent Integration: A functional AI Agent layer that handles intent detection, user context injection, and skill orchestration without external dependencies.
  - Skill Architecture: Business logic implemented as reusable, stateless skill.md files that follow the defined patterns for deterministic execution.
  - Chat Interface: A Next.js-based chat UI that enables natural language interaction with the application functionality.
  - Architecture Preservation: All existing Phase 2 functionality (auth, DB, APIs) remains operational and unchanged after AI integration.
  - Deterministic Reasoning: The AI layer operates with rule-based or mocked reasoning without external LLM dependencies, ensuring reliability and control.

**Version**: 1.2.0 | **Ratified**: TODO(RATIFICATION_DATE): Needs to be provided | **Last Amended**: 2026-01-17