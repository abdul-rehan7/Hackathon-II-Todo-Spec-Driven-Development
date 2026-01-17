# Skill Specification: list_todos

**File**: skills/list_todos.skill.md
**Created**: 2026-01-17
**Status**: Draft

## Purpose

Retrieve todos for a user. This skill is designed to be invoked by an AI Agent that has already authenticated the user and extracted any relevant filter parameters from natural language input. The skill returns todos that belong to the specified user, optionally filtered by status and priority.

## Input Parameters

### Required Parameters
- **user_id** (string): The authenticated user's unique identifier, provided by the AI Agent

### Optional Parameters
- **status** (enum: all | pending | completed): Filter todos by completion status (defaults to all if not specified)
- **priority** (enum: low | medium | high): Filter todos by priority level (returns all priority levels if not specified)
- **due_date_filter** (enum: overdue | today | upcoming | anytime): Filter todos by due date relative to current date (defaults to anytime if not specified)

## Behavior Rules

### Validation Requirements
- **User Validation**: The skill must verify that the user_id corresponds to an existing user
- **Filter Validation**: If provided, all filter parameters must be valid enum values
- **Type Validation**: All provided parameters must be of the correct type

### Processing Rules
- **Stateless Operation**: The skill must not maintain any state between invocations
- **Read-Only Access**: The skill must only read data, not modify any todos
- **Deterministic Output**: Given identical inputs, the skill must always produce the same output
- **Ownership Enforcement**: The skill must only return todos that belong to the specified user_id
- **Filter Application**: The skill must apply all provided filters simultaneously (AND logic)

### Output Requirements
- **Success Case**: Return structured output with the list of matching todos
- **Error Case**: Return structured error message with specific validation failure details
- **Consistent Format**: All todos in the response must follow the same standardized format

## Expected Output Format

### Success Response
```json
{
  "success": true,
  "message": "Todos retrieved successfully",
  "count": 0,
  "todos": [
    {
      "id": "string",
      "title": "string",
      "description": "string | null",
      "priority": "low | medium | high",
      "due_date": "ISO string | null",
      "completed": boolean,
      "created_at": "ISO string",
      "updated_at": "ISO string"
    }
  ],
  "filters_applied": {
    "status": "all | pending | completed | null",
    "priority": "low | medium | high | null",
    "due_date_filter": "overdue | today | upcoming | anytime | null"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error_code": "VALIDATION_ERROR | USER_NOT_FOUND | SYSTEM_ERROR",
  "message": "Descriptive error message",
  "validation_errors": [
    {
      "field": "field_name",
      "error": "specific error message"
    }
  ]
}
```

## Implementation Constraints

- **No Authentication Logic**: The skill assumes the AI Agent has already authenticated the user
- **No Authorization Logic**: The skill only enforces ownership via user_id (no additional authorization checks needed)
- **No HTTP Logic**: The skill is a pure business logic function
- **No UI Logic**: The skill does not handle presentation concerns
- **No External AI Dependencies**: The skill operates deterministically without external AI services
- **Database Integration**: The skill must query the existing todo database system
- **Read-Only Operations**: The skill must not modify any data

## Usage Context

This skill is designed to be invoked exclusively by an AI Agent that:
1. Has authenticated the user
2. Has parsed natural language input to extract any relevant filter parameters
3. Provides the user_id as part of the invocation context
4. Handles the response to provide appropriate feedback to the user
5. Ensures proper user ownership enforcement through the skill

## Dependencies

- Existing database system for todo persistence
- Existing todo data model/schema
- Database connection/transaction management utilities