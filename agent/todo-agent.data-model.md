# Data Model: todo-agent

**Feature**: todo-agent
**Date**: 2026-01-17

## Overview

The todo-agent primarily acts as an orchestrator between user input and skills, so it doesn't maintain its own persistent data models. However, it works with several transient data structures during the processing of user requests.

## Entity Definitions

### 1. AgentRequest (Transient)
Represents a request received by the todo-agent from the chat interface

**Fields**:
- `message`: String - The raw natural language input from the user
- `user_context`: Object - Contains authenticated user information
  - `user_id`: String - The authenticated user's unique identifier
  - `session_id`: String (Optional) - Identifier for the current conversation session
- `timestamp`: DateTime - When the request was received
- `metadata`: Object (Optional) - Additional request metadata

**Validation Rules**:
- `message` must not be empty
- `user_context` must contain a valid `user_id`
- `timestamp` defaults to current time

### 2. IntentClassificationResult (Transient)
Represents the result of the intent classification process

**Fields**:
- `intent`: String - The identified intent (CREATE_TODO, UPDATE_TODO, DELETE_TODO, LIST_TODOS)
- `confidence`: Float - Confidence score of the classification (0.0 to 1.0)
- `extracted_parameters`: Object - Parameters extracted from the natural language
- `matched_patterns`: Array of Objects - Patterns that contributed to the classification
- `classification_timestamp`: DateTime - When the classification was performed

**Validation Rules**:
- `intent` must be one of the recognized intent types
- `confidence` must be between 0.0 and 1.0
- `extracted_parameters` must match the expected format for the identified intent

### 3. SkillInvocationRequest (Transient)
Represents a request to invoke a specific skill with extracted parameters

**Fields**:
- `skill_name`: String - Name of the skill to invoke
- `parameters`: Object - Parameters to pass to the skill
- `user_context`: Object - User context to inject into the skill
- `invocation_timestamp`: DateTime - When the invocation was initiated

**Validation Rules**:
- `skill_name` must correspond to an available skill
- `parameters` must match the expected schema for the skill
- `user_context` must be valid

### 4. AgentResponse (Transient)
Represents the final response to be returned to the user

**Fields**:
- `success`: Boolean - Whether the operation was successful
- `message`: String - Natural language response for the user
- `intent`: String - The intent that was processed
- `action_taken`: Object (Optional) - Details about the action performed
- `response_timestamp`: DateTime - When the response was generated
- `error_details`: Object (Optional) - Details about any errors that occurred

**Validation Rules**:
- `success` and `message` must always be present
- If `success` is false, `error_details` should provide context
- `message` should be appropriate for chat UI display

## Integration with Existing Models

### User Model (Existing)
- No changes required
- Agent uses existing user authentication and identification

### Todo Model (Existing)
- No changes required
- Agent orchestrates skills that operate on existing todo models
- All todo operations respect existing validation rules and relationships

## State Transitions

### Agent Request Lifecycle
1. **Received**: Raw user input is captured from the chat interface
2. **Processed**: Intent classification and parameter extraction occurs
3. **Dispatched**: Appropriate skill is invoked with extracted parameters
4. **Completed**: Skill response is formatted and returned to user

### Intent Classification Process
1. **Analyzed**: Raw message is analyzed against known patterns
2. **Scored**: Confidence scores are calculated for each potential intent
3. **Selected**: Highest-confidence intent is selected (above threshold)
4. **Validated**: Extracted parameters are validated against intent requirements

## Relationships

The agent components interact in a linear flow:
```
AgentRequest → IntentClassificationResult → SkillInvocationRequest → AgentResponse
```

## Data Validation Rules

### Security Validation
- All operations must validate user ownership of referenced todos
- Input sanitization applied to prevent injection attacks
- Authentication verified before processing any requests

### Business Logic Validation
- Intent classification requires minimum confidence threshold
- Skill parameters validated against defined schemas
- User context maintained throughout the operation