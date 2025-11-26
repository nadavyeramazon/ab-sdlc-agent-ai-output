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
    Unit tests for delete_all() repository method.
    
    Tests the Delete All Tasks feature at the repository layer.
    """
    
    def test_delete_all_successfully_deletes_all_tasks(self, temp_repo):
        """
        Test that delete_all() successfully removes all tasks from the repository.
        
        Verifies that:
        1. Tasks exist before delete_all() is called
        2. After delete_all(), get_all() returns an empty list
        3. Individual task retrieval returns None for deleted tasks
        """
        # Create multiple tasks
        task1 = temp_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        task2 = temp_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        task3 = temp_repo.create(TaskCreate(title="Task 3", description="Description 3"))
        
        # Verify tasks exist
        all_tasks_before = temp_repo.get_all()
        assert len(all_tasks_before) == 3
        
        # Delete all tasks
        temp_repo.delete_all()
        
        # Verify all tasks are deleted
        all_tasks_after = temp_repo.get_all()
        assert len(all_tasks_after) == 0
        assert all_tasks_after == []
        
        # Verify individual tasks cannot be retrieved
        assert temp_repo.get_by_id(task1.id) is None
        assert temp_repo.get_by_id(task2.id) is None
        assert temp_repo.get_by_id(task3.id) is None
    
    def test_delete_all_returns_correct_count(self, temp_repo):
        """
        Test that delete_all() returns the correct count of deleted tasks.
        
        Verifies that:
        1. delete_all() returns the number of tasks that were deleted
        2. The count matches the number of tasks that existed before deletion
        3. Works correctly with different quantities of tasks
        """
        # Test with no tasks
        count_empty = temp_repo.delete_all()
        assert count_empty == 0
        
        # Create 5 tasks
        for i in range(5):
            temp_repo.create(TaskCreate(title=f"Task {i}", description=f"Description {i}"))
        
        # Verify count before deletion
        assert len(temp_repo.get_all()) == 5
        
        # Delete all and verify count
        count_deleted = temp_repo.delete_all()
        assert count_deleted == 5
        
        # Verify repository is empty
        assert len(temp_repo.get_all()) == 0
        
        # Create 2 more tasks
        temp_repo.create(TaskCreate(title="New Task 1", description="Desc 1"))
        temp_repo.create(TaskCreate(title="New Task 2", description="Desc 2"))
        
        # Delete all again and verify count
        count_deleted_2 = temp_repo.delete_all()
        assert count_deleted_2 == 2
        assert len(temp_repo.get_all()) == 0
    
    def test_delete_all_works_with_empty_database(self, temp_repo):
        """
        Test that delete_all() works correctly when database is already empty.
        
        Verifies that:
        1. delete_all() can be called on an empty repository without errors
        2. Returns count of 0 when no tasks exist
        3. Repository remains in a valid state after the operation
        4. Can still create tasks after calling delete_all() on empty database
        """
        # Verify repository starts empty
        assert len(temp_repo.get_all()) == 0
        
        # Call delete_all() on empty repository
        count = temp_repo.delete_all()
        
        # Verify count is 0
        assert count == 0
        
        # Verify repository is still empty and functional
        assert len(temp_repo.get_all()) == 0
        
        # Verify we can still create tasks after delete_all() on empty database
        new_task = temp_repo.create(TaskCreate(title="Test Task", description="Test"))
        assert new_task is not None
        assert len(temp_repo.get_all()) == 1
        
        # Verify the created task is retrievable
        retrieved_task = temp_repo.get_by_id(new_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == new_task.id
        assert retrieved_task.title == "Test Task"
