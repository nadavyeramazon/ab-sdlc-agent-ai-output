import { useState } from 'react';
import './App.css';
import logo from './assets/logo-swiftpay.png';
import { useTasks } from './hooks/useTasks';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import { taskApi } from './services/api';

function App() {
  // Use custom hook for task management
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskComplete,
    refreshTasks,
  } = useTasks();

  // Local state for edit mode
  const [editingTask, setEditingTask] = useState(null);
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState('');
  const [toggleLoading, setToggleLoading] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(null);
  const [deleteAllLoading, setDeleteAllLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  // Handle task creation
  const handleCreateTask = async (taskData) => {
    setCreateLoading(true);
    setCreateError('');

    const success = await createTask(taskData);

    setCreateLoading(false);
    if (!success) {
      setCreateError(error || 'Failed to create task');
    }

    return success;
  };

  // Handle task update
  const handleUpdateTask = async (taskData) => {
    if (!editingTask) return false;

    setEditLoading(true);
    setEditError('');

    const success = await updateTask(editingTask.id, taskData);

    setEditLoading(false);

    if (success) {
      setEditingTask(null);
    } else {
      setEditError(error || 'Failed to update task');
    }

    return success;
  };

  // Handle task deletion
  const handleDeleteTask = async (taskId) => {
    setDeleteLoading(taskId);
    await deleteTask(taskId);
    setDeleteLoading(null);
  };

  // Handle task toggle
  const handleToggleTask = async (taskId, currentStatus) => {
    setToggleLoading(taskId);
    await toggleTaskComplete(taskId, currentStatus);
    setToggleLoading(null);
  };

  // Handle delete all tasks
  const handleDeleteAllTasks = async () => {
    if (tasks.length === 0) {
      return;
    }

    const confirmed = window.confirm(
      'Are you sure you want to delete all tasks? This action cannot be undone.'
    );

    if (!confirmed) {
      return;
    }

    setDeleteAllLoading(true);
    setSuccessMessage('');

    try {
      const response = await fetch('http://localhost:3000/api/tasks/all', {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete all tasks');
      }

      const data = await response.json();

      // Refresh the task list
      await refreshTasks();

      // Show success message
      setSuccessMessage(
        `Successfully deleted ${data.deletedCount} task${data.deletedCount !== 1 ? 's' : ''}`
      );

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
    } catch (err) {
      setCreateError('Failed to delete all tasks: ' + err.message);
    } finally {
      setDeleteAllLoading(false);
    }
  };

  // Start editing a task
  const startEditTask = (task) => {
    setEditingTask(task);
    setEditError('');
  };

  // Cancel editing
  const cancelEdit = () => {
    setEditingTask(null);
    setEditError('');
  };

  return (
    <div className="app">
      <div className="container">
        <div className="app-header">
          <img src={logo} alt="Task Manager Logo" className="app-logo" />
          <h1>Task Manager</h1>
        </div>

        {/* Task List Section */}
        <div className="task-manager-section">
          <h2>My Tasks</h2>

          {/* Task Creation or Edit Form */}
          <div className="task-form-section">
            <h3>{editingTask ? 'Edit Task' : 'Create New Task'}</h3>
            <TaskForm
              onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
              onCancel={editingTask ? cancelEdit : null}
              loading={editingTask ? editLoading : createLoading}
              error={editingTask ? editError : createError}
              initialData={editingTask}
              isEditing={!!editingTask}
            />
          </div>

          {/* Task List */}
          <div className="task-list-section">
            <div className="task-list-header">
              <h3>Task List</h3>
              {tasks.length > 0 && (
                <button
                  onClick={handleDeleteAllTasks}
                  disabled={deleteAllLoading || loading}
                  className="btn-delete-all"
                >
                  {deleteAllLoading ? 'Deleting...' : 'Delete All Tasks'}
                </button>
              )}
            </div>

            {successMessage && (
              <div className="success-message">{successMessage}</div>
            )}

            <TaskList
              tasks={tasks}
              loading={loading}
              error={error}
              onToggleComplete={handleToggleTask}
              toggleLoading={toggleLoading}
              onDelete={handleDeleteTask}
              deleteLoading={deleteLoading}
              onEdit={startEditTask}
              editLoading={editLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
