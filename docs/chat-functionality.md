# AI-Powered Conversational Todo Interface Documentation

## Overview
The AI-powered conversational todo interface allows users to manage their todos using natural language commands through a chat interface. This system consists of an intelligent agent that processes natural language, interprets user intent, and executes appropriate actions using specialized skills.

## Architecture

### Components
1. **AI Agent** (`backend/src/agents/agent.py`)
   - Main orchestrator that processes user messages
   - Handles intent classification and skill selection
   - Manages conversation flow and error handling

2. **Intent Classifier** (`backend/src/agents/intent_classifier.py`)
   - Uses pattern matching to identify user intent
   - Supports CREATE_TODO, UPDATE_TODO, DELETE_TODO, and QUERY_TODOS intents
   - Provides confidence scores for classifications

3. **Skills System** (`backend/src/skills/`)
   - Modular, reusable business logic components
   - Each skill handles specific todo operations
   - Follows a consistent interface contract

4. **Chat API** (`backend/src/api/v1/chat.py`)
   - RESTful endpoint for chat interactions
   - Enforces authentication and authorization
   - Integrates with the AI agent system

5. **Frontend Components** (`frontend/src/components/ChatInterface/`)
   - Interactive chat interface for users
   - Real-time messaging with loading states
   - Confirmation dialogs for destructive actions

## Supported Commands

### Todo Creation
- "Create a new task to buy groceries"
- "Add a task to schedule meeting with John"
- "Make a new reminder to call mom"
- "Create a high priority task to finish report"
- "Set up an appointment for tomorrow"

### Todo Management
- "Update the grocery list to include milk"
- "Change the meeting time to 3 PM"
- "Mark grocery shopping as complete"
- "Finish the presentation task"
- "Delete the old appointment"
- "Remove the outdated reminder"

### Todo Queries
- "Show me my tasks"
- "What do I have scheduled for today?"
- "List my high priority tasks"
- "Show me completed tasks"
- "Find urgent todos"
- "What are my upcoming tasks?"

## Technical Details

### Intent Classification
The system uses rule-based pattern matching with regular expressions to classify user intents:

- **CREATE_TODO**: Recognizes creation commands with keywords like "create", "add", "make", "new", etc.
- **UPDATE_TODO**: Identifies update commands with keywords like "update", "change", "modify", etc.
- **DELETE_TODO**: Detects deletion/completion commands with keywords like "delete", "remove", "complete", "finish", etc.
- **QUERY_TODOS**: Matches query commands with keywords like "show", "list", "display", "find", etc.

### Skill Interface
All skills implement the `SkillInterface` which defines:
- `name`: Unique identifier for the skill
- `description`: Human-readable description
- `input_schema`: JSON schema for expected parameters
- `execute(user_id, parameters)`: Method to execute the skill

### Security
- All chat endpoints require authentication via JWT tokens
- Users can only operate on their own todos
- Input sanitization prevents injection attacks
- Confirmation dialogs for destructive actions

### Error Handling
- Graceful fallback responses for unrecognized commands
- Parameter validation for all skill executions
- Proper error messaging to users
- Logging for debugging purposes

## API Endpoints

### POST /api/v1/chat/
Process a chat message and return an AI-generated response.

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "response": "string",
  "intent": "string",
  "confidence": "float",
  "action_taken": "object"
}
```

**Authentication Required:** Bearer token in Authorization header

## Frontend Integration

### Chat Window Component
The main chat interface component that:
- Displays conversation history
- Provides input area for user messages
- Handles API communication
- Shows loading states and error messages

### Message Bubble Component
Displays individual chat messages with:
- Different styling for user vs system messages
- Timestamps
- Action details when available

### Input Area Component
Handles user input with:
- Validation
- Loading states
- Submission handling
- Helpful placeholder text

## Testing

### Unit Tests
Located in `backend/tests/`:
- `test_agent.py`: Tests for AI Agent functionality
- `test_intent_classifier.py`: Tests for intent classification
- `test_skills.py`: Tests for individual skills
- `test_chat_api.py`: Tests for chat API endpoints

### Component Tests
Located in `frontend/tests/`:
- `chat-components.test.tsx`: Tests for UI components

## Deployment Notes
- Ensure the chat API is properly secured behind authentication
- Monitor response times for AI processing
- Set up proper logging for troubleshooting
- Configure rate limiting to prevent abuse

## Troubleshooting

### Common Issues
1. **Authentication errors**: Verify JWT tokens are properly configured
2. **Intent misclassification**: Check patterns in intent_classifier.py
3. **Database errors**: Verify database connections and permissions
4. **Frontend errors**: Check browser console for JavaScript errors

### Debugging Tips
- Enable detailed logging in the AI agent
- Use the `/chat/intents/` endpoint to verify supported intents
- Check database permissions for user-specific data access
- Verify CORS settings for frontend/backend communication