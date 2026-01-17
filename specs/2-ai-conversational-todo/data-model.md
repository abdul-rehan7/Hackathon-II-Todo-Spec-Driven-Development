# Data Model: AI-Powered Conversational Todo Interface

**Feature**: 2-ai-conversational-todo
**Date**: 2026-01-17

## Overview

This document describes the data models and structures for the AI-powered conversational todo interface. The implementation preserves all existing data models while introducing new entities for chat interactions and AI processing.

## Entity Definitions

### 1. ChatMessage (New)
Represents a conversational exchange between user and AI agent

**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to User) - Links to authenticated user
- `message_content`: String (Max 2000 characters) - The raw user input or system response
- `message_type`: Enum ['user_input', 'system_response'] - Distinguishes between user and system messages
- `intent`: String (Max 100 characters) - Classified intent from natural language processing
- `timestamp`: DateTime - When the message was created
- `session_id`: UUID (Optional) - Groups related conversations (future use)

**Validation Rules**:
- `user_id` must reference an existing user
- `message_content` must not be empty
- `message_type` must be one of the allowed values
- `timestamp` defaults to current time

**Relationships**:
- Belongs to one User
- Part of a chat session (optional)

### 2. IntentClassification (New)
Represents the interpreted purpose of a user's natural language input

**Fields**:
- `id`: UUID (Primary Key)
- `name`: String (Max 100 characters) - Unique identifier for the intent type
- `description`: String (Max 500 characters) - Human-readable description of the intent
- `patterns`: Array of Strings - Regex patterns that trigger this intent
- `associated_skill`: String (Max 100 characters) - Maps to the skill that handles this intent

**Validation Rules**:
- `name` must be unique
- `patterns` must be valid regex expressions
- `associated_skill` must reference an existing skill

**Relationships**:
- Used by ChatMessage for intent classification

### 3. SkillDefinition (New)
Represents a reusable business logic unit that performs specific todo operations

**Fields**:
- `id`: UUID (Primary Key)
- `name`: String (Max 100 characters) - Unique skill identifier
- `description`: String (Max 500 characters) - Purpose of the skill
- `input_schema`: JSON - Expected input parameters for the skill
- `output_schema`: JSON - Expected output format
- `is_active`: Boolean - Whether the skill is currently enabled

**Validation Rules**:
- `name` must be unique
- `input_schema` and `output_schema` must be valid JSON
- `is_active` defaults to true

**Relationships**:
- Associated with IntentClassifications that trigger it

## State Transitions

### ChatMessage Lifecycle
1. **Created**: When user submits a message in the chat interface
2. **Processed**: When AI Agent analyzes the intent and prepares response
3. **Responded**: When system generates a response and sends back to user

### Intent Classification Process
1. **Received**: Raw user input is captured
2. **Analyzed**: Patterns are matched against known intents
3. **Mapped**: Intent is linked to appropriate skill
4. **Executed**: Skill is invoked with extracted parameters

## Relationships

```
User (1) <---> (Many) ChatMessage
ChatMessage (Many) --> (1) IntentClassification
IntentClassification (Many) --> (1) SkillDefinition
```

## Integration with Existing Models

### User Model (Existing)
- No changes required
- `chat_messages` relationship added (reverse foreign key)

### Todo Model (Existing)
- No changes required
- Skills will operate on existing todos through existing API endpoints
- Authentication and user scoping maintained through existing mechanisms

## Data Validation Rules

### Security Validation
- All operations must validate user ownership of referenced todos
- Input sanitization applied to prevent injection attacks
- Authentication verified before processing any chat messages

### Business Logic Validation
- Todo operations respect existing validation rules (due dates, priority ranges, etc.)
- Intent classification validates required parameters before skill execution
- Skill inputs are validated against defined schemas

## Future Extensions

### Session Management (Future Enhancement)
- `session_id` in ChatMessage supports grouping related conversations
- Would enable contextual understanding across multiple exchanges
- Would support multi-turn conversations for complex operations

### Analytics (Future Enhancement)
- Additional fields could track conversation effectiveness
- Metrics for intent recognition accuracy
- User satisfaction indicators