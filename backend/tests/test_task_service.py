"""
Unit tests for TaskService.

This test suite verifies the business logic layer of the task management system.
"""

from unittest.mock import MagicMock

import pytest

from app.models.task import Task, TaskCreate, TaskUpdate
from app.services.task_service import TaskService


@pytest.fixture
def mock_repository():
    """Create a mock TaskRepository for testing"""
    return MagicMock()


@pytest.fixture
def task_service(mock_repository):
    """Create a TaskService instance with mocked repository"""
    return TaskService(repository=mock_repository)


class TestTaskServiceGetAllTasks:
    """Tests for get_all_tasks method"""

    def test_get_all_tasks_returns_repository_data(self, task_service, mock_repository):
        """Test that get_all_tasks returns data from repository"""
        expected_tasks = [
            Task(
                id="1",
                title="Task 1",
                description="Description 1",
                completed=False,
                created_at="2024-01-01T00:00:00.000000Z",
                updated_at="2024-01-01T00:00:00.000000Z"
            ),
            Task(
                id="2",
                title="Task 2",
                description="Description 2",
                completed=True,
                created_at="2024-01-02T00:00:00.000000Z",
                updated_at="2024-01-02T00:00:00.000000Z"
            )
        ]
        mock_repository.get_all.return_value = expected_tasks

        result = task_service.get_all_tasks()

        assert result == expected_tasks
        mock_repository.get_all.assert_called_once()


class TestTaskServiceGetTaskById:
    """Tests for get_task_by_id method"""

    def test_get_task_by_id_returns_task(self, task_service, mock_repository):
        """Test that get_task_by_id returns task from repository"""
        task_id = "test-id"
        expected_task = Task(
            id=task_id,
            title="Test Task",
            description="Test Description",
            completed=False,
            created_at="2024-01-01T00:00:00.000000Z",
            updated_at="2024-01-01T00:00:00.000000Z"
        )
        mock_repository.get_by_id.return_value = expected_task

        result = task_service.get_task_by_id(task_id)

        assert result == expected_task
        mock_repository.get_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_returns_none_when_not_found(self, task_service, mock_repository):
        """Test that get_task_by_id returns None for non-existent task"""
        task_id = "non-existent"
        mock_repository.get_by_id.return_value = None

        result = task_service.get_task_by_id(task_id)

        assert result is None
        mock_repository.get_by_id.assert_called_once_with(task_id)


class TestTaskServiceCreateTask:
    """Tests for create_task method"""

    def test_create_task_creates_task_in_repository(self, task_service, mock_repository):
        """Test that create_task calls repository create method"""
        task_data = TaskCreate(title="New Task", description="New Description")
        expected_task = Task(
            id="new-id",
            title="New Task",
            description="New Description",
            completed=False,
            created_at="2024-01-01T00:00:00.000000Z",
            updated_at="2024-01-01T00:00:00.000000Z"
        )
        mock_repository.create.return_value = expected_task

        result = task_service.create_task(task_data)

        assert result == expected_task
        mock_repository.create.assert_called_once_with(task_data)


class TestTaskServiceUpdateTask:
    """Tests for update_task method"""

    def test_update_task_updates_task_in_repository(self, task_service, mock_repository):
        """Test that update_task calls repository update method"""
        task_id = "test-id"
        task_data = TaskUpdate(title="Updated Title", completed=True)
        expected_task = Task(
            id=task_id,
            title="Updated Title",
            description="Original Description",
            completed=True,
            created_at="2024-01-01T00:00:00.000000Z",
            updated_at="2024-01-01T01:00:00.000000Z"
        )
        mock_repository.update.return_value = expected_task

        result = task_service.update_task(task_id, task_data)

        assert result == expected_task
        mock_repository.update.assert_called_once_with(task_id, task_data)

    def test_update_task_returns_none_when_not_found(self, task_service, mock_repository):
        """Test that update_task returns None for non-existent task"""
        task_id = "non-existent"
        task_data = TaskUpdate(title="Updated Title")
        mock_repository.update.return_value = None

        result = task_service.update_task(task_id, task_data)

        assert result is None
        mock_repository.update.assert_called_once_with(task_id, task_data)


class TestTaskServiceDeleteTask:
    """Tests for delete_task method"""

    def test_delete_task_deletes_task_in_repository(self, task_service, mock_repository):
        """Test that delete_task calls repository delete method"""
        task_id = "test-id"
        mock_repository.delete.return_value = True

        result = task_service.delete_task(task_id)

        assert result is True
        mock_repository.delete.assert_called_once_with(task_id)

    def test_delete_task_returns_false_when_not_found(self, task_service, mock_repository):
        """Test that delete_task returns False for non-existent task"""
        task_id = "non-existent"
        mock_repository.delete.return_value = False

        result = task_service.delete_task(task_id)

        assert result is False
        mock_repository.delete.assert_called_once_with(task_id)


class TestTaskServiceDeleteAllTasks:
    """Tests for delete_all_tasks method"""

    def test_delete_all_tasks_calls_repository(self, task_service, mock_repository):
        """Test that delete_all_tasks calls repository delete_all method"""
        mock_repository.delete_all.return_value = 5

        result = task_service.delete_all_tasks()

        assert result == 5
        mock_repository.delete_all.assert_called_once()

    def test_delete_all_tasks_returns_zero_when_no_tasks(self, task_service, mock_repository):
        """Test that delete_all_tasks returns 0 when no tasks exist"""
        mock_repository.delete_all.return_value = 0

        result = task_service.delete_all_tasks()

        assert result == 0
        mock_repository.delete_all.assert_called_once()

    def test_delete_all_tasks_returns_count(self, task_service, mock_repository):
        """Test that delete_all_tasks returns correct count of deleted tasks"""
        expected_count = 10
        mock_repository.delete_all.return_value = expected_count

        result = task_service.delete_all_tasks()

        assert result == expected_count
        mock_repository.delete_all.assert_called_once()

    def test_delete_all_tasks_propagates_repository_exception(
        self, task_service, mock_repository
    ):
        """Test that delete_all_tasks propagates exceptions from repository"""
        mock_repository.delete_all.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            task_service.delete_all_tasks()

        mock_repository.delete_all.assert_called_once()


class TestTaskServiceIntegration:
    """Integration tests for TaskService with full workflow"""

    def test_create_and_delete_all_workflow(self, task_service, mock_repository):
        """Test complete workflow: create multiple tasks then delete all"""
        # Setup mock to simulate creating tasks
        task1 = Task(
            id="1",
            title="Task 1",
            description="Desc 1",
            completed=False,
            created_at="2024-01-01T00:00:00.000000Z",
            updated_at="2024-01-01T00:00:00.000000Z"
        )
        task2 = Task(
            id="2",
            title="Task 2",
            description="Desc 2",
            completed=False,
            created_at="2024-01-02T00:00:00.000000Z",
            updated_at="2024-01-02T00:00:00.000000Z"
        )

        mock_repository.create.side_effect = [task1, task2]
        mock_repository.get_all.side_effect = [[task1, task2], []]
        mock_repository.delete_all.return_value = 2

        # Create tasks
        created1 = task_service.create_task(TaskCreate(title="Task 1", description="Desc 1"))
        created2 = task_service.create_task(TaskCreate(title="Task 2", description="Desc 2"))

        assert created1 == task1
        assert created2 == task2

        # Verify tasks exist
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 2

        # Delete all tasks
        deleted_count = task_service.delete_all_tasks()
        assert deleted_count == 2

        # Verify no tasks remain
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 0

        # Verify repository methods were called correctly
        assert mock_repository.create.call_count == 2
        assert mock_repository.get_all.call_count == 2
        mock_repository.delete_all.assert_called_once()
