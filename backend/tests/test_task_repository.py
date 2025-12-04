"""
Property-based tests for TaskRepository.

This test suite uses Hypothesis for property-based testing to verify
correctness properties of the task repository implementation.
"""

import os

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.models.task import TaskCreate
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


@pytest.fixture
def test_repo():
    """
    Create a TaskRepository for testing with test database.
    Cleans up all tasks before and after each test.
    """
    # Use test database configuration
    os.environ["DB_NAME"] = os.getenv("TEST_DB_NAME", "taskmanager_test")

    repo = TaskRepository()

    # Clean up any existing tasks before test
    with repo._get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks")
        connection.commit()
        cursor.close()

    yield repo

    # Clean up after test
    with repo._get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks")
        connection.commit()
        cursor.close()


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
        # Use test database configuration
        os.environ["DB_NAME"] = os.getenv("TEST_DB_NAME", "taskmanager_test")

        repo = TaskRepository()

        # Clean up before test
        with repo._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks")
            connection.commit()
            cursor.close()

        try:
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

        finally:
            # Clean up after test
            with repo._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tasks")
                connection.commit()
                cursor.close()


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
        # Use test database configuration
        os.environ["DB_NAME"] = os.getenv("TEST_DB_NAME", "taskmanager_test")

        try:
            # Create first repository instance and add tasks
            repo1 = TaskRepository()

            # Clean up before test
            with repo1._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tasks")
                connection.commit()
                cursor.close()

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

            # Simulate restart by creating a new repository instance
            repo2 = TaskRepository()

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

        finally:
            # Clean up after test
            repo = TaskRepository()
            with repo._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tasks")
                connection.commit()
                cursor.close()
