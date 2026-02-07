"""
Chat API endpoint for the AI-powered conversational todo interface.

This module defines the API endpoints for chat interactions with the AI agent.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import uuid
from ...models.user import User
from ...auth import get_current_user
from ...agents.agent import AIAgent
from ...agents.intent_classifier import IntentClassifier
from ...skills.todo_create_skill import todo_create_skill
from ...skills.todo_update_skill import todo_update_skill
from ...skills.todo_delete_skill import todo_delete_skill
from ...skills.todo_query_skill import todo_query_skill
from ...utils.logging_utils import chat_logger
from pydantic import BaseModel


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    intent: str
    confidence: float
    action_taken: Dict[str, Any]


# Initialize the AI Agent with the intent classifier and skills
intent_classifier = IntentClassifier()
ai_agent = AIAgent(intent_classifier=intent_classifier)

# Register all skills with the agent
ai_agent.register_skill(todo_create_skill)
ai_agent.register_skill(todo_update_skill)
ai_agent.register_skill(todo_delete_skill)
ai_agent.register_skill(todo_query_skill)


@router.post("/chat/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Process a chat message from the user and return an AI-generated response.

    Args:
        chat_request: The chat message from the user
        current_user: The currently authenticated user

    Returns:
        ChatResponse containing the AI's response and metadata
    """
    try:
        # Log the incoming message
        chat_logger.log_interaction(
            user_id=current_user.id,
            message=chat_request.message,
            response="Processing...",
            intent="PENDING",
            confidence=0.0
        )

        # Process the message with the AI agent
        result = ai_agent.process_message(
            user_id=current_user.id,
            message=chat_request.message
        )

        # Log the completed interaction
        chat_logger.log_interaction(
            user_id=current_user.id,
            message=chat_request.message,
            response=result["response"],
            intent=result["intent"],
            confidence=result.get("confidence", 0.0),
            action_taken=result.get("action_taken", {}),
            error=None
        )

        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            confidence=result.get("confidence", 0.0),
            action_taken=result.get("action_taken", {})
        )

    except Exception as e:
        # Log the error
        chat_logger.log_error(
            user_id=current_user.id,
            message=chat_request.message,
            error=e,
            context="chat_endpoint"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )


# Endpoint to get supported intents (for debugging/testing purposes)
@router.get("/chat/intents/")
async def get_supported_intents() -> Dict[str, Any]:
    """
    Get a list of supported intents for the chat system.

    Returns:
        Dictionary containing supported intents
    """
    if hasattr(intent_classifier, 'get_supported_intents'):
        return {"intents": intent_classifier.get_supported_intents()}
    else:
        return {"intents": []}