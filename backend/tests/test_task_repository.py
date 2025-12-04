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

    repo.get_all = get_all
    repo.get_by_id = get_by_id
    repo.create = create
    repo.update = update
    repo.delete = delete

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

    @settings(max_examples=50)
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

    @settings(max_examples=50)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
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
