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


class TestDeleteAllOperation:
    """
    Property-based tests for the delete_all operation.
    
    **Feature: task-manager-app, Delete All Tasks**
    **Validates: Requirements for bulk deletion of tasks**
    """
    
    @settings(max_examples=100)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_delete_all_returns_count(self, tasks_data):
        """
        Property: For any set of tasks in the repository, delete_all should
        return the exact count of tasks that were deleted.
        
        **Feature: task-manager-app, Delete All Tasks**
        **Validates: delete_all returns count of deleted tasks**
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Create tasks
            for task_data in tasks_data:
                repo.create(task_data)
            
            # Get the count of tasks before deletion
            tasks_before = repo.get_all()
            expected_count = len(tasks_before)
            
            # Delete all tasks and verify return count
            deleted_count = repo.delete_all()
            
            assert deleted_count == expected_count
            assert deleted_count == len(tasks_data)
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    @settings(max_examples=100)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_delete_all_clears_all_tasks(self, tasks_data):
        """
        Property: For any set of tasks in the repository, after calling delete_all,
        the repository should contain no tasks (get_all returns empty list).
        
        **Feature: task-manager-app, Delete All Tasks**
        **Validates: delete_all removes all tasks from repository**
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Create tasks
            created_task_ids = []
            for task_data in tasks_data:
                task = repo.create(task_data)
                created_task_ids.append(task.id)
            
            # Verify tasks were created
            tasks_before = repo.get_all()
            assert len(tasks_before) == len(tasks_data)
            
            # Delete all tasks
            repo.delete_all()
            
            # Verify all tasks are deleted
            tasks_after = repo.get_all()
            assert len(tasks_after) == 0
            assert tasks_after == []
            
            # Verify individual tasks no longer exist
            for task_id in created_task_ids:
                task = repo.get_by_id(task_id)
                assert task is None
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_delete_all_on_empty_repository(self):
        """
        Test: Calling delete_all on an empty repository should return 0
        and the repository should remain empty.
        
        **Feature: task-manager-app, Delete All Tasks**
        **Validates: delete_all on empty repository returns 0**
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            repo = TaskRepository(data_file=temp_file)
            
            # Verify repository is empty
            tasks_before = repo.get_all()
            assert len(tasks_before) == 0
            
            # Delete all tasks (on empty repository)
            deleted_count = repo.delete_all()
            
            # Should return 0
            assert deleted_count == 0
            
            # Verify repository is still empty
            tasks_after = repo.get_all()
            assert len(tasks_after) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    @settings(max_examples=100)
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_delete_all_persists_across_restart(self, tasks_data):
        """
        Property: After calling delete_all, a new repository instance using the
        same data file should also show empty tasks (deletion is persisted).
        
        **Feature: task-manager-app, Delete All Tasks**
        **Validates: delete_all persists across repository restarts**
        """
        # Create a temporary file for persistence
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create first repository instance and add tasks
            repo1 = TaskRepository(data_file=temp_file)
            for task_data in tasks_data:
                repo1.create(task_data)
            
            # Verify tasks were created
            tasks_before = repo1.get_all()
            assert len(tasks_before) == len(tasks_data)
            
            # Delete all tasks
            repo1.delete_all()
            
            # Verify tasks are deleted in current instance
            tasks_after_delete = repo1.get_all()
            assert len(tasks_after_delete) == 0
            
            # Simulate restart by creating a new repository instance
            repo2 = TaskRepository(data_file=temp_file)
            
            # Verify the new instance also shows empty tasks
            tasks_in_new_repo = repo2.get_all()
            assert len(tasks_in_new_repo) == 0
            assert tasks_in_new_repo == []
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
