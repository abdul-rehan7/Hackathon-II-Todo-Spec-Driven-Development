# Skill Specification: update_todo

**File**: skills/update_todo.skill.md
**Created**: 2026-01-17
**Status**: Draft

## Purpose

Update an existing todo item. This skill is designed to be invoked by an AI Agent that has already authenticated the user and extracted relevant parameters from natural language input. The skill enforces ownership via user_id to ensure users can only update their own todos.

## Input Parameters

### Required Parameters
- **user_id** (string): The authenticated user's unique identifier, provided by the AI Agent
- **todo_id** (string): The unique identifier of the todo item to update

### Optional Parameters (at least one must be provided)
- **title** (string): New title for the todo item
- **description** (string): New description for the todo item
- **priority** (enum: low | medium | high): New priority level for the todo item
- **due_date** (ISO string): New due date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:mm:ss.sssZ)
- **completed** (boolean): New completion status for the todo item

## Behavior Rules

### Validation Requirements
- **Ownership Validation**: The skill must verify that the todo belongs to the provided user_id before allowing updates
- **Existence Validation**: The skill must verify that the todo_id refers to an existing todo item
- **Input Validation**: At least one optional parameter must be provided for the update
- **Priority Validation**: If priority is provided, it must be one of the allowed values (low, medium, high)
- **Date Format Validation**: If due_date is provided, it must conform to ISO 8601 format
- **Type Validation**: All provided parameters must be of the correct type

### Processing Rules
- **Stateless Operation**: The skill must not maintain any state between invocations
- **Deterministic Output**: Given identical inputs, the skill must always produce the same output
- **Ownership Enforcement**: The skill must enforce that the user can only update their own todos
- **Partial Updates**: The skill must allow updating only the specified fields while leaving others unchanged

### Output Requirements
- **Success Case**: Return structured output with the updated todo's details and confirmation
- **Error Case**: Return structured error message with specific validation failure details
- **Data Integrity**: Updated todo must be persisted to the database before returning success

## Expected Output Format

### Success Response
```json
{
  "success": true,
  "todo_id": "string",
  "message": "Todo updated successfully",
  "todo_details": {
    "title": "string",
    "description": "string | null",
    "priority": "low | medium | high",
    "due_date": "ISO string | null",
    "completed": boolean,
    "user_id": "string"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error_code": "VALIDATION_ERROR | OWNERSHIP_ERROR | NOT_FOUND_ERROR | SYSTEM_ERROR",
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
- **Database Integration**: The skill must update the existing todo in the database system

## Usage Context

This skill is designed to be invoked exclusively by an AI Agent that:
1. Has authenticated the user
2. Has parsed natural language input to extract the required parameters
3. Provides the user_id as part of the invocation context
4. Handles the response to provide appropriate feedback to the user
5. Ensures proper user ownership enforcement through the skill

## Dependencies

- Existing database system for todo persistence
- Existing todo data model/schema
- Database connection/transaction management utilities