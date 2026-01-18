"""
Intent classifier for the AI-powered conversational todo interface.

This module implements pattern-based intent classification to identify
user intentions from natural language input without relying on external LLMs.
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum


class IntentType(Enum):
    """Enumeration of supported intent types."""
    CREATE_TODO = "CREATE_TODO"
    UPDATE_TODO = "UPDATE_TODO"
    DELETE_TODO = "DELETE_TODO"
    QUERY_TODOS = "QUERY_TODOS"
    UNKNOWN = "UNKNOWN"


class IntentClassifier:
    """
    Rule-based intent classifier that uses pattern matching to identify user intent.

    This classifier implements the keyword-based and pattern-matching approach
    decided in research.md, providing deterministic behavior as required.
    """

    def __init__(self):
        """Initialize the intent classifier with predefined patterns."""
        self.patterns = {
            IntentType.CREATE_TODO: [
                (r'.*\b(create|add|make|new|set up|schedule|plan)\b.*\b(todo|task|to-do|thing|item|do|appointment|reminder)\b.*', 0.9),
                (r'.*\b(add|create)\b.*\b(task|todo)\b.*', 0.85),
                (r'.*\b(make|set up)\b.*\b(reminder|appointment)\b.*', 0.85),
                (r'.*\b(new)\b.*\b(item|thing to do)\b.*', 0.8),
                # More specific patterns for natural language commands
                (r'.*\b(create|add|make|new|set up|schedule|plan)\b.*\b(to )?(buy|call|meet|work on|prepare|finish|complete|do|get|pick up|send|write|read|watch|attend|organize|clean|fix|order|pay|cook|exercise|study|learn|review|start|begin|launch|implement|execute|perform|carry out|undertake|achieve|reach|attend|visit)\b.*', 0.95),
                (r'.*\b(i need to|i want to|i have to|i should|i must|i will|i shall|time to|going to|need to|want to|have to|should|must|will|shall|gonna|wanna|gotta|got to)\b.*\b(buy|call|meet|work on|prepare|finish|complete|do|get|pick up|send|write|read|watch|attend|organize|clean|fix|order|pay|cook|exercise|study|practice|learn|teach|review|approve|reject|confirm|cancel|start|begin|launch|implement|execute|perform|carry out|undertake|accomplish|achieve|reach|attend|visit)\b.*', 0.9),
                (r'.*\b(todo|task|to-do|thing|item|do|appointment|reminder)\b.*\b(i need to|i want to|i have to|i should|i must|i will|i shall|time to|going to|need to|want to|have to|should|must|will|shall|gonna|wanna|gotta|got to)\b.*', 0.85),
            ],
            IntentType.UPDATE_TODO: [
                (r'.*\b(update|change|modify|edit|adjust|update the|change the|modify the|edit the|adjust the)\b.*\b(todo|task|to-do|thing|item|description|details|priority|due date|title)\b.*', 0.85),
                (r'.*\b(modify|edit|change)\b.*\b(task|todo)\b.*', 0.8),
                (r'.*\b(change|update|modify)\b.*\b(the )?(description|details|priority|due date|title|status)\b.*', 0.75),
                (r'.*\b(make|set|update|change)\b.*\b(priorit|import|urg|secondar|low)\b.*', 0.7),
            ],
            IntentType.DELETE_TODO: [
                (r'.*\b(delete|remove|cancel|eliminate|get rid of|scrub|erase|wipe|clear|discard|throw away|trash|dispose of)\b.*\b(todo|task|to-do|thing|item)\b.*', 0.9),
                (r'.*\b(complete|finish|done|mark as done|check off|tick off|complete the|finish the|done with)\b.*\b(task|todo)\b.*', 0.85),
                (r'.*\b(remove|delete|get rid of|eliminate)\b.*\b(item|entry|the )', 0.8),
                (r'.*\b(cross off|check off|mark as done|complete|finish)\b.*\b(my |the )?(list|todos|tasks|to-dos)\b.*', 0.8),
            ],
            IntentType.QUERY_TODOS: [
                (r'.*\b(show|list|display|see|view|find|get|tell me|what)\b.*\b(my)?\b(todos|tasks|to-dos|things|items)\b.*', 0.9),
                (r'.*\b(what do i have|what are my|show my|list my|see my|view my|get my|fetch my|retrieve my)\b.*', 0.85),
                (r'.*\b(today|tomorrow|this week|this weekend|tonight|upcoming|later|soon|next week|next month|this month|this year)\b.*', 0.75),
                (r'.*\b(high priority|urgent|important|critical|top priority|must do|need to do|should do|have to do|immediate|asap|as soon as possible)\b.*', 0.7),
                (r'.*\b(uncompleted|incomplete|pending|not done|not finished|not completed|remaining|left to do|still to do|yet to do)\b.*', 0.7),
                (r'.*\b(completed|finished|done|marked as done|already done|already completed|completed earlier|past tasks|accomplished|achieved)\b.*', 0.7),
            ]
        }

    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of the given text.

        Args:
            text: The natural language text to classify

        Returns:
            Dictionary containing the classified intent, confidence score, and associated skill
        """
        # Normalize the text for comparison
        normalized_text = self._normalize_text(text)

        best_intent = IntentType.UNKNOWN
        best_confidence = 0.0
        matched_patterns = []

        # Check each intent type against the text
        for intent_type, pattern_list in self.patterns.items():
            for pattern, base_confidence in pattern_list:
                if re.search(pattern, normalized_text, re.IGNORECASE):
                    # Calculate confidence based on pattern match
                    confidence = base_confidence

                    # Boost confidence if multiple patterns match
                    if intent_type == best_intent:
                        confidence = min(0.99, confidence * 1.1)  # Cap at 0.99

                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent_type
                        matched_patterns.append((pattern, confidence))

        # Map intent to appropriate skill
        skill_mapping = {
            IntentType.CREATE_TODO: "todo_create_skill",
            IntentType.UPDATE_TODO: "todo_update_skill",
            IntentType.DELETE_TODO: "todo_delete_skill",
            IntentType.QUERY_TODOS: "todo_query_skill",
            IntentType.UNKNOWN: None
        }

        return {
            "intent": best_intent.value,
            "skill_name": skill_mapping.get(best_intent),
            "confidence": best_confidence,
            "matched_patterns": [pattern for pattern, _ in matched_patterns],
            "parameters": self._extract_parameters(text, best_intent)
        }

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for consistent pattern matching.

        Args:
            text: The text to normalize

        Returns:
            Normalized text
        """
        # Convert to lowercase and normalize whitespace
        normalized = ' '.join(text.lower().split())

        # Expand common contractions
        normalized = normalized.replace("i'm", "i am")
        normalized = normalized.replace("don't", "do not")
        normalized = normalized.replace("won't", "will not")
        normalized = normalized.replace("can't", "cannot")
        normalized = normalized.replace("n't", " not")

        return normalized

    def _extract_parameters(self, text: str, intent: IntentType) -> Dict[str, Any]:
        """
        Extract relevant parameters from the text based on the detected intent.

        Args:
            text: The original text
            intent: The detected intent type

        Returns:
            Dictionary containing extracted parameters
        """
        parameters = {}

        if intent in [IntentType.CREATE_TODO, IntentType.UPDATE_TODO, IntentType.QUERY_TODOS]:
            # Extract the main content of the todo
            # Look for content after action words
            content_patterns = [
                r'(?:create|add|make|new|set up|schedule|plan|update|change|modify|edit|adjust|show|list|display|see|view|find|get|tell me|what).*?\b(todo|task|to-do|thing|item|do|appointment|reminder)\b\s+(.+?)(?:\.|$)',
                r'(?:add|create|new|make)\s+(.+?)(?:\s+for|\s+by|\s+on|\s+at|\.|$)',
                r'(?:to|that|should)\s+(do|buy|call|meet|work on|prepare|finish|complete)\s+(.+?)(?:\s+for|\s+by|\s+on|\s+at|\.|$)',
            ]

            for pattern in content_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    # The content could be in different groups depending on the pattern
                    content = match.group(len(match.groups())) if match.groups() else ""
                    if not content:
                        # Try to get the last non-empty group
                        for group in reversed(match.groups()):
                            if group and group.strip():
                                content = group.strip()
                                break
                    if content:
                        parameters['content'] = content
                        break

            # If no content was extracted yet, try a simpler approach
            if 'content' not in parameters:
                # Remove action words and extract the remainder
                clean_text = re.sub(r'^(create|add|make|new|set up|schedule|plan|update|change|modify|edit|adjust|show|list|display|see|view|find|get|tell me|what)\s+', '', text, flags=re.IGNORECASE)
                clean_text = re.sub(r'\b(todo|task|to-do|thing|item|do|appointment|reminder)\b\s*', '', clean_text, flags=re.IGNORECASE)

                if clean_text.strip():
                    parameters['content'] = clean_text.strip()

        # Extract date/time information
        date_patterns = [
            (r'today', 'today'),
            (r'tomorrow', 'tomorrow'),
            (r'next week', 'next_week'),
            (r'next month', 'next_month'),
            (r'in (\d+) days?', r'in_\1_days'),
            (r'on (\d{1,2}[/-]\d{1,2}[/-]?\d{2,4})', r'on_date:\1'),
            (r'by (\d{1,2}[/-]\d{1,2}[/-]?\d{2,4})', r'by_date:\1'),
            (r'by (monday|tuesday|wednesday|thursday|friday|saturday|sunday)', r'by_day:\1'),
        ]

        for pattern, replacement in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parameters['due_date'] = match.group(0) if not match.groups() else match.group(1)
                break

        # Extract priority information
        priority_patterns = {
            'high': [r'(high|top|critical|urgent|important)', r'(important)'],
            'medium': [r'(medium|normal|regular)'],
            'low': [r'(low|lowest)']
        }

        for priority, patterns in priority_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    parameters['priority'] = priority
                    break
            if 'priority' in parameters:
                break

        # Extract category/context
        category_pattern = r'\b(work|personal|shopping|health|home|family|school|business)\b'
        category_match = re.search(category_pattern, text, re.IGNORECASE)
        if category_match:
            parameters['category'] = category_match.group(1).lower()

        return parameters

    def get_supported_intents(self) -> List[str]:
        """
        Get a list of all supported intent types.

        Returns:
            List of supported intent type names
        """
        return [intent.value for intent in IntentType]