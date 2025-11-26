import { useState, useEffect } from 'react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// TaskForm Component
function TaskForm({ onSubmit, onCancel, loading, error, initialData, isEditing }) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [validationError, setValidationError] = useState('');

  // Update form when initialData changes (for edit mode)
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || '');
      setDescription(initialData.description || '');
    } else if (!isEditing) {
      // Clear form when switching back to create mode
      setTitle('');
      setDescription('');
    }
  }, [initialData, isEditing]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (!title.trim()) {
      setValidationError('Title cannot be empty');
      return;
    }
    
    setValidationError('');
    const success = await onSubmit({ title: title.trim(), description });
    
    // Clear form after successful submission (only for create mode)
    if (success && !isEditing) {
      setTitle('');
      setDescription('');
    }
  };

  const handleCancel = () => {
    setTitle('');
    setDescription('');
    setValidationError('');
    if (onCancel) {
      onCancel();
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="task-title">Title *</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          disabled={loading}
          className={validationError ? 'input-error' : ''}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="task-description">Description</label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description (optional)"
          disabled={loading}
          rows="3"
        />
      </div>
      
      {validationError && (
        <div className="form-error">{validationError}</div>
      )}
      
      {error && (
        <div className="form-error">{error}</div>
      )}
      
      <div className="form-actions">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Task' : 'Create Task')}
        </button>
        {onCancel && (
          <button type="button" onClick={handleCancel} disabled={loading} className="btn-secondary">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

// TaskList Component
function TaskList({ 
  tasks, loading, error, 
  onToggleComplete, toggleLoading, 
  onDelete, deleteLoading, 
  onEdit, editLoading,
  onDeleteAll, deleteAllLoading
}) {
  if (loading) {
    return <div className="loading">Loading tasks...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (tasks.length === 0) {
    return <div className="no-tasks">No tasks yet</div>;
  }

  return (
    <>
      {tasks.length > 0 && (
        <div className="delete-all-container">
          <button
            onClick={onDeleteAll}
            disabled={deleteAllLoading || loading}
            className="btn-delete-all"
            aria-label="Delete all tasks"
          >
            {deleteAllLoading ? 'Deleting All...' : '🗑️ Delete All Tasks'}
          </button>
        </div>
      )}
      <div className="task-list">
        {tasks.map((task) => (
          <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
            <div className="task-header">
              <div className="task-header-left">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => onToggleComplete(task.id, task.completed)}
                  disabled={toggleLoading === task.id || deleteLoading === task.id || editLoading === task.id}
                  className="task-checkbox"
                  aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
                />
                <h3 className={task.completed ? 'task-title completed' : 'task-title'}>
                  {task.title}
                </h3>
              </div>
              <div className="task-actions">
                <span className="task-status">
                  {task.completed ? '✓ Completed' : '○ Incomplete'}
                </span>
                <button
                  onClick={() => onEdit(task)}
                  disabled={deleteLoading === task.id || toggleLoading === task.id || editLoading === task.id}
                  className="btn-edit"
                  aria-label={`Edit task "${task.title}"`}
                >
                  Edit
                </button>
                <button
                  onClick={() => onDelete(task.id)}
                  disabled={deleteLoading === task.id || toggleLoading === task.id || editLoading === task.id}
                  className="btn-delete"
                  aria-label={`Delete task "${task.title}"`}
                >
                  {deleteLoading === task.id ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
            {task.description && (
              <p className="task-description">{task.description}</p>
            )}
            <div className="task-footer">
              <span className="task-date">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

function App() {
  // Task manager state
  const [tasks, setTasks] = useState([]);
  const [tasksLoading, setTasksLoading] = useState(false);
  const [tasksError, setTasksError] = useState('');
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState('');
  const [toggleLoading, setToggleLoading] = useState(null); // Track which task is being toggled
  const [toggleError, setToggleError] = useState('');
  const [deleteLoading, setDeleteLoading] = useState(null); // Track which task is being deleted
  const [deleteError, setDeleteError] = useState('');
  const [editingTask, setEditingTask] = useState(null); // Track which task is being edited
  const [editLoading, setEditLoading] = useState(null); // Track which task is being updated
  const [editError, setEditError] = useState('');
  const [deleteAllLoading, setDeleteAllLoading] = useState(false);
  const [deleteAllError, setDeleteAllError] = useState('');

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  // Fetch all tasks from backend
  const fetchTasks = async () => {
    setTasksLoading(true);
    setTasksError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setTasks(data.tasks || []);
    } catch (err) {
      setTasksError(`Failed to fetch tasks: ${err.message}`);
    } finally {
      setTasksLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData) => {
    setCreateLoading(true);
    setCreateError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });
      
      if (!response.ok) {
        if (response.status === 422) {
          const errorData = await response.json();
          throw new Error(errorData.detail?.[0]?.msg || 'Validation error');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const newTask = await response.json();
      setTasks([newTask, ...tasks]);
      return true;
    } catch (err) {
      setCreateError(err.message);
      return false;
    } finally {
      setCreateLoading(false);
    }
  };

  // Toggle task completion status
  const toggleTaskComplete = async (taskId, currentStatus) => {
    setToggleLoading(taskId);
    setToggleError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !currentStatus }),
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Task not found. It may have been deleted.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const updatedTask = await response.json();
      
      // Update the task in the list
      setTasks(tasks.map(task => 
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      setToggleError(err.message);
      // Optionally refresh the task list on error
      setTimeout(() => setToggleError(''), 5000); // Clear error after 5 seconds
    } finally {
      setToggleLoading(null);
    }
  };

  // Delete a task
  const deleteTask = async (taskId) => {
    setDeleteLoading(taskId);
    setDeleteError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          // Task already deleted, just remove from UI
          setTasks(tasks.filter(task => task.id !== taskId));
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Remove task from UI immediately after successful deletion
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setDeleteError(err.message);
      setTimeout(() => setDeleteError(''), 5000); // Clear error after 5 seconds
    } finally {
      setDeleteLoading(null);
    }
  };

  // Delete all tasks
  const deleteAllTasks = async () => {
    if (!window.confirm('Are you sure you want to delete ALL tasks? This action cannot be undone.')) {
      return;
    }

    setDeleteAllLoading(true);
    setDeleteAllError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      setTasks([]);
    } catch (err) {
      setDeleteAllError(err.message);
      setTimeout(() => setDeleteAllError(''), 5000);
    } finally {
      setDeleteAllLoading(false);
    }
  };

  // Start editing a task
  const startEditTask = (task) => {
    setEditingTask(task);
    setEditError('');
  };

  // Update a task
  const updateTask = async (taskData) => {
    if (!editingTask) return false;

    setEditLoading(editingTask.id);
    setEditError('');

    try {
      const response = await fetch(`${API_URL}/api/tasks/${editingTask.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });
      
      if (!response.ok) {
        if (response.status === 422) {
          const errorData = await response.json();
          throw new Error(errorData.detail?.[0]?.msg || 'Validation error');
        }
        if (response.status === 404) {
          throw new Error('Task not found. It may have been deleted.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const updatedTask = await response.json();
      
      // Update the task in the list
      setTasks(tasks.map(task => 
        task.id === editingTask.id ? updatedTask : task
      ));
      
      // Clear editing state
      setEditingTask(null);
      return true;
    } catch (err) {
      setEditError(err.message);
      return false;
    } finally {
      setEditLoading(null);
    }
  };

  // Cancel editing
  const cancelEdit = () => {
    setEditingTask(null);
    setEditError('');
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Task Manager</h1>
        
        {/* Task List Section */}
        <div className="task-manager-section">
          <h2>My Tasks</h2>
          
          {/* Task Creation or Edit Form */}
          <div className="task-form-section">
            <h3>{editingTask ? 'Edit Task' : 'Create New Task'}</h3>
            <TaskForm 
              onSubmit={editingTask ? updateTask : createTask} 
              onCancel={editingTask ? cancelEdit : null}
              loading={editingTask ? editLoading !== null : createLoading} 
              error={editingTask ? editError : createError}
              initialData={editingTask}
              isEditing={!!editingTask}
            />
          </div>
          
          {/* Task List */}
          <div className="task-list-section">
            <h3>Task List</h3>
            {toggleError && (
              <div className="error" style={{ marginBottom: '1rem' }}>{toggleError}</div>
            )}
            {deleteError && (
              <div className="error" style={{ marginBottom: '1rem' }}>{deleteError}</div>
            )}
            {deleteAllError && (
              <div className="error" style={{ marginBottom: '1rem' }}>{deleteAllError}</div>
            )}
            <TaskList 
              tasks={tasks} 
              loading={tasksLoading} 
              error={tasksError}
              onToggleComplete={toggleTaskComplete}
              toggleLoading={toggleLoading}
              onDelete={deleteTask}
              deleteLoading={deleteLoading}
              onEdit={startEditTask}
              editLoading={editLoading}
              onDeleteAll={deleteAllTasks}
              deleteAllLoading={deleteAllLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
