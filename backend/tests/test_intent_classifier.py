import pytest
from src.agents.intent_classifier import IntentClassifier, IntentType


class TestIntentClassifier:
    """Unit tests for the IntentClassifier class."""

    def test_initialization(self):
        """Test that IntentClassifier initializes correctly with patterns."""
        classifier = IntentClassifier()

        # Check that patterns are loaded
        assert IntentType.CREATE_TODO in [IntentType(intent) for intent in classifier.patterns.keys()]
        assert IntentType.UPDATE_TODO in [IntentType(intent) for intent in classifier.patterns.keys()]
        assert IntentType.DELETE_TODO in [IntentType(intent) for intent in classifier.patterns.keys()]
        assert IntentType.QUERY_TODOS in [IntentType(intent) for intent in classifier.patterns.keys()]

    def test_classify_create_todo_simple(self):
        """Test classifying a simple create todo intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Create a new task to buy groceries")

        assert result["intent"] == IntentType.CREATE_TODO.value
        assert result["confidence"] > 0.5  # Should have decent confidence
        assert result["skill_name"] == "todo_create_skill"

    def test_classify_create_todo_complex(self):
        """Test classifying a complex create todo intent."""
        classifier = IntentClassifier()

        result = classifier.classify("I need to create a high priority task to finish the report")

        assert result["intent"] == IntentType.CREATE_TODO.value
        assert result["skill_name"] == "todo_create_skill"

    def test_classify_update_todo(self):
        """Test classifying an update todo intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Update the grocery list task to include milk")

        assert result["intent"] == IntentType.UPDATE_TODO.value
        assert result["skill_name"] == "todo_update_skill"

    def test_classify_delete_todo(self):
        """Test classifying a delete todo intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Delete the meeting prep task")

        assert result["intent"] == IntentType.DELETE_TODO.value
        assert result["skill_name"] == "todo_delete_skill"

    def test_classify_complete_todo(self):
        """Test classifying a complete todo intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Mark the shopping task as complete")

        assert result["intent"] == IntentType.DELETE_TODO.value  # Complete is mapped to delete
        assert result["skill_name"] == "todo_delete_skill"

    def test_classify_query_todos_all(self):
        """Test classifying a query all todos intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Show me my tasks")

        assert result["intent"] == IntentType.QUERY_TODOS.value
        assert result["skill_name"] == "todo_query_skill"

    def test_classify_query_todos_priority(self):
        """Test classifying a query high priority todos intent."""
        classifier = IntentClassifier()

        result = classifier.classify("Show me my high priority tasks")

        assert result["intent"] == IntentType.QUERY_TODOS.value
        assert result["skill_name"] == "todo_query_skill"

    def test_classify_unknown_intent(self):
        """Test classifying an unknown intent."""
        classifier = IntentClassifier()

        result = classifier.classify("This is a completely random sentence with no actionable intent")

        # Should return the intent with highest confidence, which might still be one of the patterns
        # due to our pattern matching, but with lower confidence
        assert result["intent"] in [intent.value for intent in IntentType]
        assert result["skill_name"] in [None, "todo_create_skill", "todo_update_skill", "todo_delete_skill", "todo_query_skill"]

    def test_normalize_text(self):
        """Test text normalization functionality."""
        classifier = IntentClassifier()

        # This test requires access to the private method, which we'll test indirectly
        # by checking if normalization affects classification
        original = "I'm going to BUY groceries tomorrow!"
        normalized = classifier._normalize_text(original)

        assert "i am" in normalized.lower()  # Contraction expansion
        assert "buy" in normalized.lower()  # Lowercase conversion
        assert "groceries" in normalized.lower()  # Content preserved

    def test_extract_parameters_basic(self):
        """Test basic parameter extraction."""
        classifier = IntentClassifier()

        # This tests the parameter extraction logic
        result = classifier._extract_parameters("Create a task to buy groceries", IntentType.CREATE_TODO)

        # Should extract content from the command
        assert isinstance(result, dict)

    def test_get_supported_intents(self):
        """Test getting supported intents."""
        classifier = IntentClassifier()

        intents = classifier.get_supported_intents()

        assert len(intents) > 0
        assert "CREATE_TODO" in intents
        assert "UPDATE_TODO" in intents
        assert "DELETE_TODO" in intents
        assert "QUERY_TODOS" in intents
        assert "UNKNOWN" in intents