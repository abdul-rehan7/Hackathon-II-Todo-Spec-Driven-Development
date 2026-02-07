"""
Logging utilities for the AI-powered conversational todo interface.

This module provides logging functionality for chat interactions and system events.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class LogLevel(Enum):
    """Enumeration for different log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ChatLogger:
    """Logger specifically for chat interactions."""

    def __init__(self, name: str = "chat_logger"):
        """Initialize the chat logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_interaction(
        self,
        user_id: str,
        message: str,
        response: str,
        intent: str,
        confidence: float,
        action_taken: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        """Log a chat interaction."""
        interaction_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "message": message,
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "action_taken": action_taken or {},
            "error": error
        }

        log_level = LogLevel.ERROR if error else LogLevel.INFO
        self.logger.info(f"CHAT_INTERACTION: {json.dumps(interaction_data)}")

    def log_intent_classification(
        self,
        user_id: str,
        message: str,
        intent: str,
        confidence: float,
        matched_patterns: list
    ):
        """Log intent classification results."""
        classification_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "message": message,
            "intent": intent,
            "confidence": confidence,
            "matched_patterns": matched_patterns
        }

        self.logger.info(f"INTENT_CLASSIFIED: {json.dumps(classification_data)}")

    def log_skill_execution(
        self,
        user_id: str,
        skill_name: str,
        parameters: Dict[str, Any],
        success: bool,
        message: str = "",
        error: Optional[str] = None
    ):
        """Log skill execution."""
        execution_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "skill_name": skill_name,
            "parameters": parameters,
            "success": success,
            "message": message,
            "error": error
        }

        log_level = LogLevel.ERROR if error else LogLevel.INFO
        log_msg = f"SKILL_EXECUTED: {json.dumps(execution_data)}"

        if error:
            self.logger.error(log_msg)
        else:
            self.logger.info(log_msg)

    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """Log general system events."""
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        }

        self.logger.info(f"SYSTEM_EVENT: {json.dumps(event_data)}")

    def log_error(self, user_id: str, message: str, error: Exception, context: str = ""):
        """Log an error with context."""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "message": message,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }

        self.logger.error(f"ERROR_OCCURRED: {json.dumps(error_data)}")


# Global chat logger instance
chat_logger = ChatLogger()