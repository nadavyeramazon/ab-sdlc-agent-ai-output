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


class TestDeleteAll:
    """
    Tests for TaskRepository.delete_all() method.
    
    Verifies that delete_all() correctly removes all tasks from the repository
    and returns the appropriate count of deleted tasks.
    """
    
    def test_delete_all_returns_correct_count(self, temp_repo):
        """
        Test delete_all() returns the number of tasks deleted.
        
        Verifies that when tasks exist in the repository, delete_all()
        returns the exact count of tasks that were deleted.
        """
        # Create multiple tasks
        task1 = temp_repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        task2 = temp_repo.create(TaskCreate(title="Task 2", description="Desc 2"))
        task3 = temp_repo.create(TaskCreate(title="Task 3", description="Desc 3"))
        
        # Verify tasks were created
        assert len(temp_repo.get_all()) == 3
        
        # Delete all tasks
        deleted_count = temp_repo.delete_all()
        
        # Verify correct count returned
        assert deleted_count == 3
        
        # Verify all tasks are deleted
        assert len(temp_repo.get_all()) == 0

    def test_delete_all_empty_repository(self, temp_repo):
        """
        Test delete_all() on empty repository returns 0.
        
        Verifies that calling delete_all() when no tasks exist
        returns 0 and does not raise any errors.
        """
        # Verify repository is empty
        assert len(temp_repo.get_all()) == 0
        
        # Delete all tasks (when none exist)
        deleted_count = temp_repo.delete_all()
        
        # Verify 0 is returned
        assert deleted_count == 0
        
        # Verify repository is still empty
        assert len(temp_repo.get_all()) == 0

    def test_delete_all_persists_changes(self):
        """
        Test delete_all() changes persist across repository reload.
        
        Verifies that after calling delete_all(), creating a new
        repository instance with the same data file shows no tasks.
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create first repository instance and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            repo1.create(TaskCreate(title="Task 1", description="Desc 1"))
            repo1.create(TaskCreate(title="Task 2", description="Desc 2"))
            repo1.create(TaskCreate(title="Task 3", description="Desc 3"))
            
            # Verify tasks were created
            assert len(repo1.get_all()) == 3
            
            # Delete all tasks
            deleted_count = repo1.delete_all()
            assert deleted_count == 3
            
            # Create new repository instance with same file (simulates restart)
            repo2 = TaskRepository(data_file=temp_file)
            
            # Verify no tasks in reloaded repository
            assert len(repo2.get_all()) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_delete_all_clears_all_task_ids(self, temp_repo):
        """
        Test that delete_all() removes all tasks so individual lookups fail.
        
        Verifies that after delete_all(), attempting to get any previously
        existing task by ID returns None.
        """
        # Create multiple tasks and store their IDs
        task_ids = []
        for i in range(5):
            task = temp_repo.create(TaskCreate(title=f"Task {i+1}", description=f"Desc {i+1}"))
            task_ids.append(task.id)
        
        # Verify all tasks exist
        for task_id in task_ids:
            assert temp_repo.get_by_id(task_id) is not None
        
        # Delete all tasks
        temp_repo.delete_all()
        
        # Verify all tasks are gone (individual lookups return None)
        for task_id in task_ids:
            assert temp_repo.get_by_id(task_id) is None

    @settings(max_examples=50)
    @given(num_tasks=st.integers(min_value=0, max_value=20))
    def test_delete_all_returns_exact_count(self, num_tasks):
        """
        Property-based test: delete_all() always returns the exact count of deleted tasks.
        
        For any number of tasks in the repository, delete_all() should return
        exactly that number.
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Create the specified number of tasks
            for i in range(num_tasks):
                repo.create(TaskCreate(title=f"Task {i+1}", description=f"Desc {i+1}"))
            
            # Verify tasks were created
            assert len(repo.get_all()) == num_tasks
            
            # Delete all tasks
            deleted_count = repo.delete_all()
            
            # Verify correct count returned
            assert deleted_count == num_tasks
            
            # Verify all tasks are deleted
            assert len(repo.get_all()) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
