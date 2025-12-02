"""
Property-based tests for TaskRepository.

This test suite uses Hypothesis for property-based testing to verify
correctness properties of the task repository implementation.
"""

import pytest
import tempfile
import os
from hypothesis import given, settings, strategies as st
from task_repository import TaskRepository
from main import TaskCreate, TaskUpdate


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
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
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
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
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
            assert all_tasks[0].completed == False
            
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
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
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
                    'id': t.id,
                    'title': t.title,
                    'description': t.description,
                    'completed': t.completed,
                    'created_at': t.created_at,
                    'updated_at': t.updated_at
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
                loaded = loaded_tasks_by_id[expected['id']]
                assert loaded.id == expected['id']
                assert loaded.title == expected['title']
                assert loaded.description == expected['description']
                assert loaded.completed == expected['completed']
                assert loaded.created_at == expected['created_at']
                assert loaded.updated_at == expected['updated_at']
                
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestDeleteAllTasks:
    """
    Tests for the delete_all() method of TaskRepository.
    
    Tests cover:
    - Deleting all tasks from an empty repository
    - Deleting all tasks from a populated repository
    - Verifying the return value (count of deleted tasks)
    - Verifying persistence after delete_all
    """

    def test_delete_all_empty_repository(self, temp_repo):
        """Test delete_all on an empty repository returns 0."""
        count = temp_repo.delete_all()
        
        assert count == 0
        assert temp_repo.get_all() == []

    def test_delete_all_single_task(self, temp_repo):
        """Test delete_all removes a single task and returns 1."""
        # Create one task
        task_data = TaskCreate(title="Test Task", description="Test Description")
        temp_repo.create(task_data)
        
        # Verify task exists
        assert len(temp_repo.get_all()) == 1
        
        # Delete all tasks
        count = temp_repo.delete_all()
        
        assert count == 1
        assert temp_repo.get_all() == []

    def test_delete_all_multiple_tasks(self, temp_repo):
        """Test delete_all removes multiple tasks and returns correct count."""
        # Create multiple tasks
        for i in range(5):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            temp_repo.create(task_data)
        
        # Verify tasks exist
        assert len(temp_repo.get_all()) == 5
        
        # Delete all tasks
        count = temp_repo.delete_all()
        
        assert count == 5
        assert temp_repo.get_all() == []

    def test_delete_all_persists_empty_state(self):
        """Test that delete_all persists the empty state to file."""
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create repository and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            for i in range(3):
                task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
                repo1.create(task_data)
            
            # Verify tasks exist
            assert len(repo1.get_all()) == 3
            
            # Delete all tasks
            repo1.delete_all()
            
            # Simulate restart by creating a new repository instance
            repo2 = TaskRepository(data_file=temp_file)
            
            # Verify empty state persisted
            assert repo2.get_all() == []
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_delete_all_twice_returns_zero_second_time(self, temp_repo):
        """Test calling delete_all twice - second call returns 0."""
        # Create tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            temp_repo.create(task_data)
        
        # First delete_all
        first_count = temp_repo.delete_all()
        assert first_count == 3
        
        # Second delete_all should return 0
        second_count = temp_repo.delete_all()
        assert second_count == 0

    def test_delete_all_allows_new_tasks_after(self, temp_repo):
        """Test that new tasks can be created after delete_all."""
        # Create initial tasks
        for i in range(2):
            task_data = TaskCreate(title=f"Old Task {i}", description=f"Description {i}")
            temp_repo.create(task_data)
        
        # Delete all
        temp_repo.delete_all()
        assert temp_repo.get_all() == []
        
        # Create new tasks
        new_task = TaskCreate(title="New Task", description="New Description")
        created_task = temp_repo.create(new_task)
        
        # Verify new task exists
        all_tasks = temp_repo.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == created_task.id
        assert all_tasks[0].title == "New Task"

    @settings(max_examples=50)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=0, max_size=20))
    def test_property_delete_all_clears_all_tasks(self, tasks_data):
        """
        Property: For any set of tasks in the repository, calling delete_all
        should result in an empty task list and return the exact count of
        tasks that were deleted.
        """
        # Create a temporary repository for this test
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Create all tasks
            for task_data in tasks_data:
                repo.create(task_data)
            
            # Get count before deletion
            tasks_before = repo.get_all()
            expected_count = len(tasks_before)
            
            # Delete all tasks
            actual_count = repo.delete_all()
            
            # Verify count matches
            assert actual_count == expected_count
            
            # Verify repository is empty
            assert repo.get_all() == []
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @settings(max_examples=50)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_property_delete_all_persists_across_restart(self, tasks_data):
        """
        Property: After calling delete_all and restarting the repository,
        the empty state should persist.
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create repository and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            for task_data in tasks_data:
                repo1.create(task_data)
            
            # Verify tasks exist before deletion
            assert len(repo1.get_all()) == len(tasks_data)
            
            # Delete all tasks
            repo1.delete_all()
            
            # Simulate restart by creating a new repository instance
            repo2 = TaskRepository(data_file=temp_file)
            
            # Verify empty state persisted
            assert repo2.get_all() == []
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
