import { useState } from 'react';
import './App.css';
import logo from './assets/logo-swiftpay.png';
import { useTasks } from './hooks/useTasks';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';

function App() {
  // Use custom hook for task management
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    deleteAllTasks,
    toggleTaskComplete,
  } = useTasks();

  // Local state for edit mode
  const [editingTask, setEditingTask] = useState(null);
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState('');
  const [toggleLoading, setToggleLoading] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(null);

  // State for delete all confirmation
  const [showDeleteAllConfirm, setShowDeleteAllConfirm] = useState(false);
  const [deleteAllLoading, setDeleteAllLoading] = useState(false);

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

  // Handle delete all click
  const handleDeleteAllClick = () => {
    setShowDeleteAllConfirm(true);
  };

  // Handle delete all confirmation
  const handleDeleteAllConfirm = async () => {
    setDeleteAllLoading(true);
    await deleteAllTasks();
    setDeleteAllLoading(false);
    setShowDeleteAllConfirm(false);
  };

  // Handle delete all cancel
  const handleDeleteAllCancel = () => {
    setShowDeleteAllConfirm(false);
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
          <img src={logo} alt="SwiftPay Logo" className="app-logo" />
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

          {/* Delete All Section */}
          {tasks.length > 0 && !showDeleteAllConfirm && (
            <div className="delete-all-section">
              <button
                className="btn-danger"
                onClick={handleDeleteAllClick}
                disabled={deleteAllLoading}
              >
                {deleteAllLoading ? 'Deleting...' : 'Delete All Tasks'}
              </button>
            </div>
          )}

          {/* Delete All Confirmation */}
          {showDeleteAllConfirm && (
            <div className="delete-all-confirm">
              <p className="delete-all-warning">
                Are you sure you want to delete ALL tasks? This action cannot be
                undone.
              </p>
              <div className="delete-all-actions">
                <button className="btn-secondary" onClick={handleDeleteAllCancel}>
                  Cancel
                </button>
                <button
                  className="btn-danger-filled"
                  onClick={handleDeleteAllConfirm}
                  disabled={deleteAllLoading}
                >
                  {deleteAllLoading ? 'Deleting...' : 'Yes, Delete All'}
                </button>
              </div>
            </div>
          )}

          {/* Task List */}
          <div className="task-list-section">
            <h3>Task List</h3>
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
