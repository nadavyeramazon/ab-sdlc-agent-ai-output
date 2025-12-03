"""
Property-based tests for TaskRepository.

This test suite uses Hypothesis for property-based testing to verify
correctness properties of the task repository implementation.
"""

import os
import tempfile

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from main import TaskCreate
from task_repository import TaskRepository


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
def temp_repo():
    """
    Create a temporary TaskRepository for testing.
    Uses a temporary file that is cleaned up after the test.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        repo = TaskRepository(data_file=temp_file)
        yield repo
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)


class TestTaskCreationPersistence:
    """
    Property-based tests for task creation and persistence.

    **Feature: task-manager-app, Property 1: Task creation persistence**
    **Validates: Requirements 1.1, 1.4**
    """

    @settings(max_examples=100)
    @given(task_data=task_create_strategy())
    def test_created_task_appears_in_get_all(self, task_data):
        """
        Property: For any valid task with a non-empty title, when the task is
        created through the repository, retrieving all tasks should include the
        newly created task with matching title and description.

        **Feature: task-manager-app, Property 1: Task creation persistence**
        **Validates: Requirements 1.1, 1.4**
        """
        # Create a temporary repository for this test
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name

        try:
            repo = TaskRepository(data_file=temp_file)

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
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestPersistenceAcrossRestarts:
    """
    Property-based tests for persistence across repository restarts.

    **Feature: task-manager-app, Property 9: Persistence across restarts**
    **Validates: Requirements 7.1, 7.3**
    """

    @settings(max_examples=100)
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
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name

        try:
            # Create first repository instance and add tasks
            repo1 = TaskRepository(data_file=temp_file)
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
            repo2 = TaskRepository(data_file=temp_file)

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
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestDeleteAllMethod:
    """Unit tests for TaskRepository delete_all method"""

    def test_delete_all_empty_repository(self, temp_repo):
        """Test delete_all on an empty repository returns 0"""
        count = temp_repo.delete_all()
        assert count == 0
        assert temp_repo.get_all() == []

    def test_delete_all_single_task(self, temp_repo):
        """Test delete_all with a single task"""
        # Create a task
        task_data = TaskCreate(title="Test Task", description="Description")
        temp_repo.create(task_data)

        # Verify task exists
        assert len(temp_repo.get_all()) == 1

        # Delete all
        count = temp_repo.delete_all()
        assert count == 1
        assert temp_repo.get_all() == []

    def test_delete_all_multiple_tasks(self, temp_repo):
        """Test delete_all with multiple tasks"""
        # Create multiple tasks
        for i in range(5):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            temp_repo.create(task_data)

        # Verify tasks exist
        assert len(temp_repo.get_all()) == 5

        # Delete all
        count = temp_repo.delete_all()
        assert count == 5
        assert temp_repo.get_all() == []

    def test_delete_all_persists_to_file(self):
        """Test that delete_all persists the empty state to file"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name

        try:
            # Create repository and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            task_data = TaskCreate(title="Task 1", description="Description")
            repo1.create(task_data)

            # Delete all
            repo1.delete_all()

            # Create new repository instance (simulates restart)
            repo2 = TaskRepository(data_file=temp_file)

            # Verify no tasks exist
            assert repo2.get_all() == []

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_delete_all_idempotent(self, temp_repo):
        """Test that delete_all can be called multiple times safely"""
        # Create tasks
        task_data = TaskCreate(title="Task 1", description="Description")
        temp_repo.create(task_data)

        # First delete
        count1 = temp_repo.delete_all()
        assert count1 == 1
        assert temp_repo.get_all() == []

        # Second delete (on empty repository)
        count2 = temp_repo.delete_all()
        assert count2 == 0
        assert temp_repo.get_all() == []

        # Third delete
        count3 = temp_repo.delete_all()
        assert count3 == 0
        assert temp_repo.get_all() == []

    def test_delete_all_then_create_new_task(self, temp_repo):
        """Test that new tasks can be created after delete_all"""
        # Create and delete tasks
        task_data1 = TaskCreate(title="Task 1", description="Description 1")
        temp_repo.create(task_data1)
        temp_repo.delete_all()

        # Create new task after deletion
        task_data2 = TaskCreate(title="Task 2", description="Description 2")
        new_task = temp_repo.create(task_data2)

        # Verify only the new task exists
        all_tasks = temp_repo.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == new_task.id
        assert all_tasks[0].title == "Task 2"

    def test_delete_all_with_completed_and_incomplete_tasks(self, temp_repo):
        """Test delete_all removes both completed and incomplete tasks"""
        from main import TaskUpdate

        # Create incomplete task
        task_data1 = TaskCreate(title="Incomplete Task", description="Not done")
        task1 = temp_repo.create(task_data1)

        # Create and complete a task
        task_data2 = TaskCreate(title="Completed Task", description="Done")
        task2 = temp_repo.create(task_data2)
        update_data = TaskUpdate(completed=True)
        temp_repo.update(task2.id, update_data)

        # Verify we have 2 tasks
        assert len(temp_repo.get_all()) == 2

        # Delete all
        count = temp_repo.delete_all()
        assert count == 2
        assert temp_repo.get_all() == []


class TestDeleteAllProperties:
    """Property-based tests for delete_all method"""

    @settings(max_examples=100)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=0, max_size=20))
    def test_property_delete_all_returns_correct_count(self, tasks_data):
        """
        Property: For any set of N tasks, delete_all should return N and
        leave the repository empty.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name

        try:
            repo = TaskRepository(data_file=temp_file)

            # Create tasks
            for task_data in tasks_data:
                repo.create(task_data)

            expected_count = len(tasks_data)

            # Delete all
            actual_count = repo.delete_all()

            # Verify count matches
            assert actual_count == expected_count

            # Verify repository is empty
            assert repo.get_all() == []

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @settings(max_examples=100)
    @given(
        tasks_before=st.lists(task_create_strategy(), min_size=1, max_size=10),
        tasks_after=st.lists(task_create_strategy(), min_size=1, max_size=10),
    )
    def test_property_delete_all_clean_slate(self, tasks_before, tasks_after):
        """
        Property: After delete_all, creating new tasks should result in a
        clean slate with only the new tasks present.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name

        try:
            repo = TaskRepository(data_file=temp_file)

            # Create first batch
            for task_data in tasks_before:
                repo.create(task_data)

            # Delete all
            repo.delete_all()

            # Create second batch
            new_task_ids = []
            for task_data in tasks_after:
                task = repo.create(task_data)
                new_task_ids.append(task.id)

            # Verify only second batch exists
            all_tasks = repo.get_all()
            assert len(all_tasks) == len(tasks_after)

            retrieved_ids = {task.id for task in all_tasks}
            assert retrieved_ids == set(new_task_ids)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
