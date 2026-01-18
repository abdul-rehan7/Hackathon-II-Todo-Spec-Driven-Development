import pytest
from unittest.mock import Mock, patch, MagicMock
from src.skills.todo_create_skill import TodoCreateSkill
from src.skills.todo_update_skill import TodoUpdateSkill
from src.skills.todo_delete_skill import TodoDeleteSkill
from src.skills.todo_query_skill import TodoQuerySkill
from src.models.todo import Todo, Priority


class TestTodoCreateSkill:
    """Unit tests for the TodoCreateSkill class."""

    def test_skill_properties(self):
        """Test that the skill has the correct properties."""
        skill = TodoCreateSkill()

        assert skill.name == "todo_create_skill"
        assert "creates new todos" in skill.description.lower()
        assert "content" in skill.input_schema["properties"]
        assert "content" in skill.input_schema["required"]

    def test_validate_parameters_valid(self):
        """Test validating valid parameters."""
        skill = TodoCreateSkill()
        valid_params = {
            "content": "Buy groceries"
        }

        result = skill.validate_parameters(valid_params)

        assert result is True

    def test_validate_parameters_invalid(self):
        """Test validating invalid parameters."""
        skill = TodoCreateSkill()
        invalid_params = {
            # Missing required "content" parameter
        }

        result = skill.validate_parameters(invalid_params)

        assert result is False

    @patch('src.database.get_session')
    def test_execute_success(self, mock_get_session):
        """Test successful execution of the skill."""
        # Mock the database session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the Todo object that will be created
        mock_todo = Todo(
            id=1,
            title="Buy groceries",
            description="Buy groceries",
            completed=False,
            priority=3,  # Medium priority
            user_id="user123"
        )

        # Configure the session to return the mock todo after commit/refresh
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_todo.id = 1  # Set ID after "commit"
        mock_session.add.return_value = None

        skill = TodoCreateSkill()
        params = {
            "content": "Buy groceries",
            "priority": "medium"
        }

        result = skill.execute("user123", params)

        assert result.success is True
        assert "successfully created todo" in result.message.lower()
        assert result.data is not None
        assert result.data["todo_id"] == 1

    @patch('src.database.get_session')
    def test_execute_empty_content(self, mock_get_session):
        """Test execution with empty content."""
        skill = TodoCreateSkill()
        params = {
            "content": ""  # Empty content
        }

        result = skill.execute("user123", params)

        assert result.success is False
        assert "cannot create a todo without content" in result.message.lower()


class TestTodoUpdateSkill:
    """Unit tests for the TodoUpdateSkill class."""

    def test_skill_properties(self):
        """Test that the skill has the correct properties."""
        skill = TodoUpdateSkill()

        assert skill.name == "todo_update_skill"
        assert "updates existing todos" in skill.description.lower()
        assert "todo_id" in skill.input_schema["properties"]
        assert "todo_id" in skill.input_schema["required"]

    def test_validate_parameters_valid(self):
        """Test validating valid parameters."""
        skill = TodoUpdateSkill()
        valid_params = {
            "todo_id": 1
        }

        result = skill.validate_parameters(valid_params)

        assert result is True

    @patch('src.database.get_session')
    def test_execute_success(self, mock_get_session):
        """Test successful execution of the update skill."""
        # Mock the database session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock a todo object
        mock_todo = Todo(
            id=1,
            title="Old Title",
            description="Old Description",
            completed=False,
            priority=3,
            user_id="user123"
        )

        # Configure exec to return the mock todo
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_todo
        mock_session.exec.return_value = mock_exec_result

        skill = TodoUpdateSkill()
        params = {
            "todo_id": 1,
            "title": "Updated Title",
            "completed": True
        }

        result = skill.execute("user123", params)

        assert result.success is True
        assert "successfully updated todo" in result.message.lower()
        assert result.data is not None


class TestTodoDeleteSkill:
    """Unit tests for the TodoDeleteSkill class."""

    def test_skill_properties(self):
        """Test that the skill has the correct properties."""
        skill = TodoDeleteSkill()

        assert skill.name == "todo_delete_skill"
        assert "deletes existing todos" in skill.description.lower()
        assert "todo_id" in skill.input_schema["properties"]
        assert "todo_id" in skill.input_schema["required"]

    def test_validate_parameters_valid(self):
        """Test validating valid parameters."""
        skill = TodoDeleteSkill()
        valid_params = {
            "todo_id": 1
        }

        result = skill.validate_parameters(valid_params)

        assert result is True

    @patch('src.database.get_session')
    def test_execute_success(self, mock_get_session):
        """Test successful execution of the delete skill."""
        # Mock the database session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock a todo object
        mock_todo = Todo(
            id=1,
            title="Sample Todo",
            description="Sample Description",
            completed=False,
            priority=3,
            user_id="user123"
        )

        # Configure exec to return the mock todo
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_todo
        mock_session.exec.return_value = mock_exec_result
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        skill = TodoDeleteSkill()
        params = {
            "todo_id": 1
        }

        result = skill.execute("user123", params)

        assert result.success is True
        assert "successfully deleted todo" in result.message.lower()
        assert result.data is not None


class TestTodoQuerySkill:
    """Unit tests for the TodoQuerySkill class."""

    def test_skill_properties(self):
        """Test that the skill has the correct properties."""
        skill = TodoQuerySkill()

        assert skill.name == "todo_query_skill"
        assert "queries and retrieves" in skill.description.lower()

    @patch('src.database.get_session')
    def test_execute_success(self, mock_get_session):
        """Test successful execution of the query skill."""
        # Mock the database session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock some todo objects
        mock_todos = [
            Todo(
                id=1,
                title="Sample Todo 1",
                description="Sample Description 1",
                completed=False,
                priority=3,
                user_id="user123"
            ),
            Todo(
                id=2,
                title="Sample Todo 2",
                description="Sample Description 2",
                completed=True,
                priority=1,
                user_id="user123"
            )
        ]

        # Configure exec to return the mock todos
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = mock_todos
        mock_session.exec.return_value = mock_exec_result

        skill = TodoQuerySkill()
        params = {}  # No specific filters

        result = skill.execute("user123", params)

        assert result.success is True
        assert "you have 2" in result.message.lower()
        assert result.data is not None
        assert result.data["count"] == 2