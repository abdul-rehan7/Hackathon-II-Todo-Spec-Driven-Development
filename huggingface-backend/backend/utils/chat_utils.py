"""
Utility functions for chat operations in the AI-powered conversational todo interface.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class ChatMessageType(Enum):
    """Enumeration for different types of chat messages."""
    USER_INPUT = "user_input"
    SYSTEM_RESPONSE = "system_response"


class ChatUtils:
    """Utility class containing helper functions for chat operations."""

    @staticmethod
    def sanitize_user_input(text: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            text: The raw user input

        Returns:
            Sanitized text with potentially harmful content removed
        """
        # Remove potentially harmful characters/sequences
        sanitized = re.sub(r'[<>(){}[\]]', '', text)
        # Limit length to prevent abuse
        max_length = 2000  # As defined in quickstart.md
        return sanitized[:max_length]

    @staticmethod
    def extract_parameters_from_text(text: str) -> Dict[str, Any]:
        """
        Extract potential parameters from natural language text.

        Args:
            text: The natural language input from user

        Returns:
            Dictionary containing extracted parameters
        """
        params = {}

        # Look for date-related patterns
        date_patterns = [
            r'today',
            r'tomorrow',
            r'next week',
            r'next month',
            r'in (\d+) days?',
            r'on (\d{1,2}[/-]\d{1,2}[/-]?\d{2,4})',
            r'by (\d{1,2}[/-]\d{1,2}[/-]?\d{2,4})',
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                params['date'] = matches[0] if matches else None
                break

        # Look for priority-related patterns
        priority_patterns = {
            'high': [r'(high|top|critical|urgent|important)\s*(priority|prio|p)'],
            'medium': [r'(medium|normal|regular)\s*(priority|prio|p)'],
            'low': [r'(low|lowest)\s*(priority|prio|p)'],
        }

        for priority, patterns in priority_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    params['priority'] = priority
                    break
            if 'priority' in params:
                break

        # Look for category/context
        category_pattern = r'(work|personal|shopping|health|home|family|school)'
        category_match = re.search(category_pattern, text, re.IGNORECASE)
        if category_match:
            params['category'] = category_match.group(1).lower()

        return params

    @staticmethod
    def validate_message_length(text: str, max_length: int = 2000) -> bool:
        """
        Validate that message length is within acceptable limits.

        Args:
            text: The message text to validate
            max_length: Maximum allowed length (default 2000)

        Returns:
            True if length is valid, False otherwise
        """
        return len(text) <= max_length

    @staticmethod
    def format_timestamp(timestamp: Optional[datetime] = None) -> str:
        """
        Format a timestamp for chat messages.

        Args:
            timestamp: Optional datetime object, defaults to now

        Returns:
            ISO formatted timestamp string
        """
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.isoformat()

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text to simplify pattern matching.

        Args:
            text: The input text

        Returns:
            Text with normalized whitespace
        """
        return ' '.join(text.split())