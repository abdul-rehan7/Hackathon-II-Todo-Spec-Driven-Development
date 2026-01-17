# Skill Specification: create_todo

**File**: skills/create_todo.skill.md
**Created**: 2026-01-17
**Status**: Draft

## Purpose

Create a new todo item for an authenticated user. This skill is designed to be invoked by an AI Agent that has already authenticated the user and extracted relevant parameters from natural language input.

## Input Parameters

### Required Parameters
- **user_id** (string): The authenticated user's unique identifier, provided by the AI Agent
- **title** (string): The title of the new todo item

### Optional Parameters
- **description** (string): Detailed description of the todo item
- **priority** (enum: low | medium | high): Priority level of the todo (defaults to medium if not specified)
- **due_date** (ISO string): Due date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:mm:ss.sssZ)

## Behavior Rules

### Validation Requirements
- **Input Shape Validation**: The skill must validate that all required parameters are present and of correct type
- **Priority Validation**: If priority is provided, it must be one of the allowed values (low, medium, high)
- **Date Format Validation**: If due_date is provided, it must conform to ISO 8601 format

### Processing Rules
- **Stateless Operation**: The skill must not maintain any state between invocations
- **Deterministic Output**: Given identical inputs, the skill must always produce the same output
- **User Context**: The skill operates within the context of the provided user_id (no authorization checks needed)

### Output Requirements
- **Success Case**: Return structured output with the created todo's ID and confirmation
- **Error Case**: Return structured error message with specific validation failure details
- **Data Integrity**: Created todo must be persisted to the database before returning success

## Expected Output Format

### Success Response
```json
{
  "success": true,
  "todo_id": "string",
  "message": "Todo created successfully",
  "todo_details": {
    "title": "string",
    "description": "string | null",
    "priority": "low | medium | high",
    "due_date": "ISO string | null",
    "completed": false,
    "user_id": "string"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error_code": "VALIDATION_ERROR | SYSTEM_ERROR",
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
- **No Authorization Logic**: The skill operates within the provided user context
- **No HTTP Logic**: The skill is a pure business logic function
- **No UI Logic**: The skill does not handle presentation concerns
- **No External AI Dependencies**: The skill operates deterministically without external AI services
- **Database Integration**: The skill must persist the new todo to the existing database system

## Usage Context

This skill is designed to be invoked exclusively by an AI Agent that:
1. Has authenticated the user
2. Has parsed natural language input to extract the required parameters
3. Provides the user_id as part of the invocation context
4. Handles the response to provide appropriate feedback to the user

## Dependencies

- Existing database system for todo persistence
- Existing todo data model/schema
- Database connection/transaction management utilities