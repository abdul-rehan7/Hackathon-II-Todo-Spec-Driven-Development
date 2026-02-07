import pytest
from unittest.mock import Mock, MagicMock
from src.agents.agent import AIAgent
from src.agents.intent_classifier import IntentClassifier
from src.skills.skill_interface import SkillInterface, SkillResult
from src.skills.todo_create_skill import TodoCreateSkill


class MockSkill(SkillInterface):
    """Mock skill for testing purposes."""

    def __init__(self, name: str, should_succeed: bool = True):
        self._name = name
        self._should_succeed = should_succeed

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Mock skill for testing: {self._name}"

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def execute(self, user_id: str, parameters: dict) -> SkillResult:
        if self._should_succeed:
            return SkillResult(
                success=True,
                message=f"Successfully executed {self._name}",
                data={"result": "test_data"}
            )
        else:
            return SkillResult(
                success=False,
                message=f"Failed to execute {self._name}",
                error="Test error"
            )


class TestAIAgent:
    """Unit tests for the AIAgent class."""

    def test_initialization(self):
        """Test that AIAgent initializes correctly."""
        agent = AIAgent()

        assert agent.skills == []
        assert agent.intent_classifier is None

    def test_register_skill(self):
        """Test registering a skill with the agent."""
        agent = AIAgent()
        mock_skill = MockSkill("test_skill")

        agent.register_skill(mock_skill)

        assert len(agent.skills) == 1
        assert agent.skills[0] == mock_skill

    def test_get_skill_by_name_found(self):
        """Test getting a skill by name when it exists."""
        agent = AIAgent()
        mock_skill = MockSkill("test_skill")
        agent.register_skill(mock_skill)

        found_skill = agent.get_skill_by_name("test_skill")

        assert found_skill == mock_skill

    def test_get_skill_by_name_not_found(self):
        """Test getting a skill by name when it doesn't exist."""
        agent = AIAgent()
        mock_skill = MockSkill("test_skill")
        agent.register_skill(mock_skill)

        found_skill = agent.get_skill_by_name("nonexistent_skill")

        assert found_skill is None

    def test_process_message_with_matching_intent(self):
        """Test processing a message with a matching intent."""
        # Create a mock intent classifier
        mock_classifier = Mock()
        mock_classifier.classify.return_value = {
            "intent": "CREATE_TODO",
            "skill_name": "test_skill",
            "confidence": 0.9,
            "parameters": {"test_param": "test_value"}
        }

        # Create a mock skill
        mock_skill = MockSkill("test_skill")

        agent = AIAgent(intent_classifier=mock_classifier)
        agent.register_skill(mock_skill)

        result = agent.process_message("user123", "Create a new task")

        assert result["response"] == "Successfully executed test_skill"
        assert result["intent"] == "CREATE_TODO"
        assert result["confidence"] == 0.9
        assert result["action_taken"]["result"] == "test_data"

    def test_process_message_with_low_confidence(self):
        """Test processing a message with low confidence intent."""
        # Create a mock intent classifier
        mock_classifier = Mock()
        mock_classifier.classify.return_value = {
            "intent": "CREATE_TODO",
            "skill_name": "test_skill",
            "confidence": 0.2,  # Below threshold
            "parameters": {}
        }

        agent = AIAgent(intent_classifier=mock_classifier)

        result = agent.process_message("user123", "This is not a clear command")

        assert "I'm not sure I understood your request" in result["response"]
        assert result["intent"] == "CREATE_TODO"
        assert result["confidence"] == 0.2

    def test_process_message_with_no_matching_skill(self):
        """Test processing a message when no skill matches."""
        # Create a mock intent classifier
        mock_classifier = Mock()
        mock_classifier.classify.return_value = {
            "intent": "CREATE_TODO",
            "skill_name": "nonexistent_skill",
            "confidence": 0.9,
            "parameters": {}
        }

        agent = AIAgent(intent_classifier=mock_classifier)

        result = agent.process_message("user123", "Create a new task")

        assert "I recognize the intent 'CREATE_TODO' but I don't have the capability to handle it yet" in result["response"]

    def test_process_message_with_skill_failure(self):
        """Test processing a message when the skill fails."""
        # Create a mock intent classifier
        mock_classifier = Mock()
        mock_classifier.classify.return_value = {
            "intent": "CREATE_TODO",
            "skill_name": "failing_skill",
            "confidence": 0.9,
            "parameters": {}
        }

        # Create a mock skill that fails
        failing_skill = MockSkill("failing_skill", should_succeed=False)

        agent = AIAgent(intent_classifier=mock_classifier)
        agent.register_skill(failing_skill)

        result = agent.process_message("user123", "Create a new task")

        assert "I encountered an issue: Test error" in result["response"]