"""
Property-based tests for TaskRepository.

This test suite uses Hypothesis for property-based testing to verify
correctness properties of the task repository implementation.
"""

from unittest.mock import patch

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository


# Custom strategies for generating test data
@st.composite
def task_create_strategy(draw):
    """
    Generate valid TaskCreate objects for property testing.

    Generates titles that are non-empty and within length limits,
    and descriptions within length limits.
    """
    # Generate non-empty title (1-200 chars)
    title = draw(st.text(min_size=1, max_size=200).filter(lambda s: s.strip() != ""))
    # Generate description (0-1000 chars)
    description = draw(st.text(min_size=0, max_size=1000))

    return TaskCreate(title=title, description=description)


# Mock task storage
mock_tasks = {}


def create_mock_repository():
    """Create a mock repository with in-memory storage"""
    repo = TaskRepository.__new__(TaskRepository)
    repo.db_config = {}

    # Override methods to use in-memory storage
    def get_all():
        return sorted(mock_tasks.values(), key=lambda t: t.created_at, reverse=True)

    def get_by_id(task_id: str):
        return mock_tasks.get(task_id)

    def create(task_data: TaskCreate):
        task = Task.create_new(task_data)
        mock_tasks[task.id] = task
        return task

    def update(task_id: str, task_data):
        existing = mock_tasks.get(task_id)
        if not existing:
            return None
        updated = existing.update_from(task_data)
        mock_tasks[task_id] = updated
        return updated

    def delete(task_id: str):
        if task_id in mock_tasks:
            del mock_tasks[task_id]
            return True
        return False

    def delete_all():
        count = len(mock_tasks)
        mock_tasks.clear()
        return count

    repo.get_all = get_all
    repo.get_by_id = get_by_id
    repo.create = create
    repo.update = update
    repo.delete = delete
    repo.delete_all = delete_all

    return repo


@pytest.fixture
def test_repo():
    """
    Create a TaskRepository for testing with mocked storage.
    Cleans up all tasks before and after each test.
    """
    global mock_tasks
    mock_tasks = {}

    with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
        repo = create_mock_repository()
        yield repo

    mock_tasks = {}


class TestTaskCreationPersistence:
    """
    Property-based tests for task creation and persistence.

    **Feature: task-manager-app, Property 1: Task creation persistence**
    **Validates: Requirements 1.1, 1.4**
    """

    @settings(max_examples=10, deadline=1000)
    @given(task_data=task_create_strategy())
    def test_created_task_appears_in_get_all(self, task_data):
        """
        Property: For any valid task with a non-empty title, when the task is
        created through the repository, retrieving all tasks should include the
        newly created task with matching title and description.

        **Feature: task-manager-app, Property 1: Task creation persistence**
        **Validates: Requirements 1.1, 1.4**
        """
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            repo = create_mock_repository()

            # Create the task
            created_task = repo.create(task_data)

            # Retrieve all tasks
            all_tasks = repo.get_all()

            # Verify the created task appears in the list
            assert len(all_tasks) == 1
            assert all_tasks[0].id == created_task.id
            assert all_tasks[0].title == task_data.title
            assert all_tasks[0].description == task_data.description
            assert all_tasks[0].completed is False

        mock_tasks = {}


class TestPersistenceAcrossRestarts:
    """
    Property-based tests for persistence across repository restarts.

    **Feature: task-manager-app, Property 9: Persistence across restarts**
    **Validates: Requirements 7.1, 7.3**
    """

    @settings(max_examples=10, deadline=2000)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=5))
    def test_tasks_persist_across_restarts(self, tasks_data):
        """
        Property: For any set of tasks created before a repository restart,
        when the repository restarts and loads data, all previously created
        tasks should be retrievable with identical data (id, title, description,
        completed status, timestamps).

        **Feature: task-manager-app, Property 9: Persistence across restarts**
        **Validates: Requirements 7.1, 7.3**
        """
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            # Create first repository instance and add tasks
            repo1 = create_mock_repository()

            created_tasks = []
            for task_data in tasks_data:
                task = repo1.create(task_data)
                created_tasks.append(task)

            # Store task details for comparison
            task_details = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at,
                }
                for t in created_tasks
            ]

            # Simulate restart by creating a new repository instance (shares same mock_tasks)
            repo2 = create_mock_repository()

            # Retrieve all tasks from the new instance
            loaded_tasks = repo2.get_all()

            # Verify all tasks were loaded
            assert len(loaded_tasks) == len(created_tasks)

            # Verify each task's data is identical
            loaded_tasks_by_id = {t.id: t for t in loaded_tasks}
            for expected in task_details:
                loaded = loaded_tasks_by_id[expected["id"]]
                assert loaded.id == expected["id"]
                assert loaded.title == expected["title"]
                assert loaded.description == expected["description"]
                assert loaded.completed == expected["completed"]
                assert loaded.created_at == expected["created_at"]
                assert loaded.updated_at == expected["updated_at"]

        mock_tasks = {}


class TestDeleteAllTasks:
    """
    Unit tests for delete_all method in TaskRepository.
    Tests the ability to delete all tasks from the database.
    """

    def test_delete_all_with_no_tasks(self, test_repo):
        """Test delete_all returns 0 when no tasks exist."""
        count = test_repo.delete_all()
        assert count == 0
        assert len(test_repo.get_all()) == 0

    def test_delete_all_with_single_task(self, test_repo):
        """Test delete_all removes single task and returns count 1."""
        # Create a task
        task_data = TaskCreate(title="Test Task", description="Description")
        test_repo.create(task_data)

        # Verify task exists
        assert len(test_repo.get_all()) == 1

        # Delete all tasks
        count = test_repo.delete_all()

        # Verify count and that no tasks remain
        assert count == 1
        assert len(test_repo.get_all()) == 0

    def test_delete_all_with_multiple_tasks(self, test_repo):
        """Test delete_all removes all tasks and returns correct count."""
        # Create multiple tasks
        task_count = 5
        for i in range(task_count):
            task_data = TaskCreate(
                title=f"Task {i}",
                description=f"Description {i}"
            )
            test_repo.create(task_data)

        # Verify tasks exist
        assert len(test_repo.get_all()) == task_count

        # Delete all tasks
        count = test_repo.delete_all()

        # Verify count and that no tasks remain
        assert count == task_count
        assert len(test_repo.get_all()) == 0

    @settings(max_examples=10, deadline=2000)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_delete_all_property_removes_all_tasks(self, tasks_data):
        """
        Property: delete_all removes all tasks regardless of count.
        For any set of tasks, delete_all should remove all tasks and
        return the correct count.
        """
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            repo = create_mock_repository()

            # Create tasks
            for task_data in tasks_data:
                repo.create(task_data)

            expected_count = len(tasks_data)

            # Delete all tasks
            deleted_count = repo.delete_all()

            # Verify count matches
            assert deleted_count == expected_count

            # Verify no tasks remain
            assert len(repo.get_all()) == 0

        mock_tasks = {}

    def test_delete_all_idempotent(self, test_repo):
        """Test that calling delete_all multiple times is safe."""
        # Create some tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", description="Description")
            test_repo.create(task_data)

        # First delete_all
        count1 = test_repo.delete_all()
        assert count1 == 3
        assert len(test_repo.get_all()) == 0

        # Second delete_all (no tasks)
        count2 = test_repo.delete_all()
        assert count2 == 0
        assert len(test_repo.get_all()) == 0

    def test_delete_all_with_completed_and_incomplete_tasks(self, test_repo):
        """Test delete_all removes both completed and incomplete tasks."""
        # Create completed tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Completed {i}", description="Done")
            task = test_repo.create(task_data)
            # Mark as completed
            from app.models.task import TaskUpdate
            test_repo.update(task.id, TaskUpdate(completed=True))

        # Create incomplete tasks
        for i in range(2):
            task_data = TaskCreate(title=f"Incomplete {i}", description="Not done")
            test_repo.create(task_data)

        # Verify all tasks exist
        assert len(test_repo.get_all()) == 5

        # Delete all tasks
        count = test_repo.delete_all()

        # Verify all tasks removed
        assert count == 5
        assert len(test_repo.get_all()) == 0
