"""
Base AI Agent class for the conversational todo interface.

This class implements the core logic for processing user input,
classifying intents, selecting appropriate skills, and executing them.
"""

from typing import Dict, Any, Optional, List
from ..utils.chat_utils import ChatUtils
from ..skills.skill_interface import SkillInterface, SkillResult
from ..utils.logging_utils import chat_logger


class AIAgent:
    """
    AI Agent responsible for processing natural language input and orchestrating skills.

    The agent follows these responsibilities as outlined in the research.md:
    - Parse incoming natural language messages
    - Classify user intent using pattern matching
    - Extract relevant parameters from user input
    - Invoke appropriate skills with validated parameters
    - Format responses for frontend display
    """

    def __init__(self, intent_classifier=None, skills: Optional[List[SkillInterface]] = None):
        """
        Initialize the AI Agent.

        Args:
            intent_classifier: Optional intent classifier instance
            skills: List of available skills for the agent to use
        """
        self.intent_classifier = intent_classifier
        self.skills = skills or []
        self.chat_utils = ChatUtils()

    def register_skill(self, skill: SkillInterface):
        """
        Register a new skill with the agent.

        Args:
            skill: Skill to register
        """
        self.skills.append(skill)

    def get_skill_by_name(self, name: str) -> Optional[SkillInterface]:
        """
        Retrieve a skill by its name.

        Args:
            name: Name of the skill to retrieve

        Returns:
            The skill instance if found, None otherwise
        """
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.

        Args:
            user_id: ID of the user sending the message
            message: Natural language message from the user

        Returns:
            Dictionary containing the response and metadata
        """
        # Sanitize the input message
        sanitized_message = self.chat_utils.sanitize_user_input(message)

        # Classify the intent
        intent_result = self.classify_intent(sanitized_message)
        intent = intent_result.get('intent')
        confidence = intent_result.get('confidence', 0.0)

        # Log intent classification
        chat_logger.log_intent_classification(
            user_id=user_id,
            message=message,
            intent=intent or "unknown",
            confidence=confidence,
            matched_patterns=intent_result.get('matched_patterns', [])
        )

        # Extract parameters from the message
        extracted_params = self.chat_utils.extract_parameters_from_text(sanitized_message)

        # Combine extracted parameters with any that were identified during intent classification
        parameters = {**extracted_params, **intent_result.get('parameters', {})}

        # If we have a recognized intent and sufficient confidence, execute the associated skill
        response = ""
        action_taken = {}

        if intent and confidence >= 0.5:  # Using a reasonable threshold
            skill = self.get_skill_by_name(intent_result.get('skill_name'))

            if skill:
                # Validate parameters before execution
                if skill.validate_parameters(parameters):
                    # Execute the skill
                    try:
                        skill_result = skill.execute(user_id, parameters)

                        # Log skill execution
                        chat_logger.log_skill_execution(
                            user_id=user_id,
                            skill_name=skill.name,
                            parameters=parameters,
                            success=skill_result.success,
                            message=skill_result.message,
                            error=skill_result.error
                        )

                        if skill_result.success:
                            response = skill_result.message
                            action_taken = skill_result.data or {}
                        else:
                            response = f"I encountered an issue: {skill_result.error or 'Unknown error'}"
                            # Log the error for debugging
                            chat_logger.log_error(
                                user_id=user_id,
                                message=message,
                                error=Exception(skill_result.error or "Unknown error"),
                                context="skill_execution"
                            )
                    except Exception as e:
                        response = f"I encountered an unexpected error while processing your request: {str(e)}"
                        # Log the error for debugging
                        chat_logger.log_error(
                            user_id=user_id,
                            message=message,
                            error=e,
                            context="skill_execution_exception"
                        )
                else:
                    response = "I couldn't understand the parameters in your request. Could you please rephrase?"
                    # Log parameter validation failure
                    chat_logger.log_skill_execution(
                        user_id=user_id,
                        skill_name=intent_result.get('skill_name', 'unknown'),
                        parameters=parameters,
                        success=False,
                        message="Parameter validation failed",
                        error="Invalid parameters provided"
                    )
            else:
                response = f"I recognize the intent '{intent}' but I don't have the capability to handle it yet."
                # Log missing skill
                chat_logger.log_error(
                    user_id=user_id,
                    message=message,
                    error=Exception(f"No skill found for intent: {intent}"),
                    context="missing_skill"
                )
        else:
            # Fallback response when intent is not clear
            response = self.generate_fallback_response(sanitized_message)
            # Log fallback case
            chat_logger.log_interaction(
                user_id=user_id,
                message=message,
                response=response,
                intent="FALLBACK",
                confidence=confidence
            )

        return {
            "response": response,
            "intent": intent or "unknown",
            "confidence": confidence,
            "action_taken": action_taken,
            "parameters_extracted": parameters
        }

    def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Classify the intent of a message using the intent classifier.

        Args:
            message: The message to classify

        Returns:
            Dictionary containing intent information
        """
        if self.intent_classifier:
            return self.intent_classifier.classify(message)
        else:
            # Fallback to a simple keyword-based classification if no classifier is provided
            return self._simple_keyword_classification(message)

    def _simple_keyword_classification(self, message: str) -> Dict[str, Any]:
        """
        Simple keyword-based intent classification as a fallback.

        Args:
            message: The message to classify

        Returns:
            Dictionary containing intent information
        """
        message_lower = message.lower()

        # Define simple keyword patterns for different intents
        if any(keyword in message_lower for keyword in [
            'create', 'add', 'make', 'new', 'set up', 'schedule', 'plan'
        ]) and any(keyword in message_lower for keyword in [
            'todo', 'task', 'to-do', 'thing', 'item', 'do', 'appointment', 'reminder'
        ]):
            return {
                "intent": "CREATE_TODO",
                "skill_name": "todo_create_skill",
                "confidence": 0.8,
                "parameters": {}
            }

        elif any(keyword in message_lower for keyword in [
            'update', 'change', 'modify', 'edit', 'adjust'
        ]) and any(keyword in message_lower for keyword in [
            'todo', 'task', 'to-do', 'thing', 'item'
        ]):
            return {
                "intent": "UPDATE_TODO",
                "skill_name": "todo_update_skill",
                "confidence": 0.7,
                "parameters": {}
            }

        elif any(keyword in message_lower for keyword in [
            'delete', 'remove', 'cancel', 'finish', 'complete', 'done', 'mark as done'
        ]) and any(keyword in message_lower for keyword in [
            'todo', 'task', 'to-do', 'thing', 'item'
        ]):
            return {
                "intent": "DELETE_TODO",
                "skill_name": "todo_delete_skill",
                "confidence": 0.7,
                "parameters": {}
            }

        elif any(keyword in message_lower for keyword in [
            'show', 'list', 'display', 'see', 'view', 'find', 'get', 'tell me', 'what'
        ]) and any(keyword in message_lower for keyword in [
            'my', 'todos', 'tasks', 'to-dos', 'things', 'items', 'today', 'tomorrow', 'week'
        ]):
            return {
                "intent": "QUERY_TODOS",
                "skill_name": "todo_query_skill",
                "confidence": 0.7,
                "parameters": {}
            }

        else:
            return {
                "intent": "UNKNOWN",
                "skill_name": None,
                "confidence": 0.0,
                "parameters": {}
            }

    def generate_fallback_response(self, message: str) -> str:
        """
        Generate a fallback response when intent cannot be determined.

        Args:
            message: The original user message

        Returns:
            Appropriate fallback response
        """
        return (
            f"I'm not sure I understood your request: '{message[:50]}{'...' if len(message) > 50 else ''}'. "
            "You can try commands like 'Create a new task to buy groceries', "
            "'Show me my tasks for today', 'Mark task 1 as complete', or "
            "'Delete the meeting prep task'."
        )