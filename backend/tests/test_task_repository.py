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


class TestDeleteAllMethod:
    """
    Comprehensive tests for TaskRepository.delete_all() method.
    
    **Feature: task-manager-app, Delete All Tasks**
    **Validates: Requirements for bulk task deletion functionality**
    """
    
    def test_delete_all_removes_all_tasks(self, temp_repo):
        """
        Test that delete_all removes all tasks from the repository.
        
        Verifies:
        - All tasks are removed from memory
        - get_all returns empty list after deletion
        - Returns correct count of deleted tasks
        """
        # Create multiple tasks
        task1 = temp_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        task2 = temp_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        task3 = temp_repo.create(TaskCreate(title="Task 3", description="Description 3"))
        
        # Verify tasks exist
        tasks_before = temp_repo.get_all()
        assert len(tasks_before) == 3
        
        # Delete all tasks
        deleted_count = temp_repo.delete_all()
        
        # Verify return value
        assert deleted_count == 3
        
        # Verify all tasks are removed
        tasks_after = temp_repo.get_all()
        assert len(tasks_after) == 0
        assert tasks_after == []
    
    def test_delete_all_on_empty_repository(self, temp_repo):
        """
        Test that delete_all handles empty repository correctly.
        
        Verifies:
        - Returns 0 when no tasks exist
        - Does not cause errors on empty repository
        - Repository remains in valid state
        """
        # Verify repository is empty
        tasks_before = temp_repo.get_all()
        assert len(tasks_before) == 0
        
        # Delete all tasks (none exist)
        deleted_count = temp_repo.delete_all()
        
        # Verify return value
        assert deleted_count == 0
        
        # Verify repository is still empty
        tasks_after = temp_repo.get_all()
        assert len(tasks_after) == 0
    
    def test_delete_all_persists_to_file(self):
        """
        Test that delete_all persists the deletion to the data file.
        
        Verifies:
        - Deletion is written to disk
        - Reloading repository shows empty state
        - File contains empty task list
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create repository and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            repo1.create(TaskCreate(title="Task 1", description="Description 1"))
            repo1.create(TaskCreate(title="Task 2", description="Description 2"))
            
            # Verify tasks exist
            assert len(repo1.get_all()) == 2
            
            # Delete all tasks
            deleted_count = repo1.delete_all()
            assert deleted_count == 2
            
            # Create new repository instance (simulates restart)
            repo2 = TaskRepository(data_file=temp_file)
            
            # Verify tasks are still deleted after restart
            tasks_after_restart = repo2.get_all()
            assert len(tasks_after_restart) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_delete_all_clears_internal_cache(self, temp_repo):
        """
        Test that delete_all clears the internal task cache.
        
        Verifies:
        - Internal _tasks dictionary is cleared
        - get_by_id returns None for previously existing tasks
        - No tasks can be retrieved after deletion
        """
        # Create tasks
        task1 = temp_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        task2 = temp_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        
        # Store task IDs
        task1_id = task1.id
        task2_id = task2.id
        
        # Verify tasks can be retrieved
        assert temp_repo.get_by_id(task1_id) is not None
        assert temp_repo.get_by_id(task2_id) is not None
        
        # Delete all tasks
        temp_repo.delete_all()
        
        # Verify tasks cannot be retrieved
        assert temp_repo.get_by_id(task1_id) is None
        assert temp_repo.get_by_id(task2_id) is None
    
    def test_delete_all_allows_new_tasks_after_deletion(self, temp_repo):
        """
        Test that new tasks can be created after delete_all.
        
        Verifies:
        - Repository remains functional after delete_all
        - New tasks can be created with fresh IDs
        - New tasks are properly persisted
        """
        # Create initial tasks
        temp_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        temp_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        
        # Delete all tasks
        deleted_count = temp_repo.delete_all()
        assert deleted_count == 2
        assert len(temp_repo.get_all()) == 0
        
        # Create new tasks after deletion
        new_task1 = temp_repo.create(TaskCreate(title="New Task 1", description="New Description 1"))
        new_task2 = temp_repo.create(TaskCreate(title="New Task 2", description="New Description 2"))
        
        # Verify new tasks exist
        tasks = temp_repo.get_all()
        assert len(tasks) == 2
        assert new_task1.title == "New Task 1"
        assert new_task2.title == "New Task 2"
    
    @settings(max_examples=50)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=20))
    def test_property_delete_all_removes_all_tasks_comprehensive(self, tasks_data):
        """
        Property-based test: delete_all removes all tasks regardless of quantity.
        
        For any non-empty set of tasks, delete_all should remove all tasks
        and return the correct count.
        
        **Feature: task-manager-app, Property: Delete all completeness**
        """
        # Create a temporary repository for this test
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Create all tasks
            for task_data in tasks_data:
                repo.create(task_data)
            
            # Verify tasks were created
            initial_count = len(repo.get_all())
            assert initial_count == len(tasks_data)
            
            # Delete all tasks
            deleted_count = repo.delete_all()
            
            # Verify all tasks were deleted
            assert deleted_count == initial_count
            assert len(repo.get_all()) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_delete_all_with_mixed_task_states(self, temp_repo):
        """
        Test delete_all removes tasks regardless of their completion state.
        
        Verifies:
        - Both completed and incomplete tasks are deleted
        - Task state doesn't affect deletion
        """
        # Create tasks with different states
        task1 = temp_repo.create(TaskCreate(title="Incomplete Task", description="Not done"))
        task2 = temp_repo.create(TaskCreate(title="Complete Task", description="Done"))
        
        # Update one task to completed
        temp_repo.update(task2.id, TaskUpdate(completed=True))
        
        # Verify both tasks exist
        tasks_before = temp_repo.get_all()
        assert len(tasks_before) == 2
        
        # Delete all tasks
        deleted_count = temp_repo.delete_all()
        
        # Verify both tasks are deleted
        assert deleted_count == 2
        assert len(temp_repo.get_all()) == 0
    
    def test_delete_all_updates_file_content(self):
        """
        Test that delete_all writes an empty array to the JSON file.
        
        Verifies:
        - JSON file is updated with empty array
        - File remains valid JSON
        - File can be read by new repository instance
        """
        import json
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create repository and add tasks
            repo = TaskRepository(data_file=temp_file)
            repo.create(TaskCreate(title="Task 1", description="Description 1"))
            repo.create(TaskCreate(title="Task 2", description="Description 2"))
            
            # Delete all tasks
            repo.delete_all()
            
            # Read file content directly
            with open(temp_file, 'r') as f:
                file_content = json.load(f)
            
            # Verify file contains empty array
            assert file_content == []
            assert isinstance(file_content, list)
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_delete_all_idempotence(self, temp_repo):
        """
        Test that calling delete_all multiple times is safe (idempotent).
        
        Verifies:
        - Multiple calls don't cause errors
        - Subsequent calls return 0
        - Repository remains in valid state
        """
        # Create tasks
        temp_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        temp_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        
        # First delete_all
        deleted_count1 = temp_repo.delete_all()
        assert deleted_count1 == 2
        assert len(temp_repo.get_all()) == 0
        
        # Second delete_all (should be safe)
        deleted_count2 = temp_repo.delete_all()
        assert deleted_count2 == 0
        assert len(temp_repo.get_all()) == 0
        
        # Third delete_all (should still be safe)
        deleted_count3 = temp_repo.delete_all()
        assert deleted_count3 == 0
        assert len(temp_repo.get_all()) == 0
