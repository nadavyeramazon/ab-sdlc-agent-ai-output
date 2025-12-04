import TaskItem from './TaskItem';

function TaskList({
  tasks,
  loading,
  error,
  onToggleComplete,
  toggleLoading,
  onDelete,
  deleteLoading,
  onEdit,
  editLoading,
  onDeleteAll,
  deleteAllLoading,
  taskCount,
}) {
  if (loading) {
    return <div className="loading">Loading tasks...</div>;
  }

  // Only show error-only state if there are no tasks to display
  // (e.g., initial fetch error)
  if (error && tasks.length === 0) {
    return <div className="error">{error}</div>;
  }

  // Show empty state when no tasks and no error
  if (tasks.length === 0 && !error) {
    return <div className="no-tasks">No tasks yet</div>;
  }

  return (
    <div>
      {/* Show error inline when there are tasks (e.g., after failed operation with rollback) */}
      {error && <div className="error">{error}</div>}

      <div className="task-list-header">
        <div></div>
        <button
          className="btn-delete-all"
          onClick={onDeleteAll}
          disabled={deleteAllLoading || taskCount === 0}
        >
          {deleteAllLoading ? 'Deleting...' : `Delete All (${taskCount})`}
        </button>
      </div>
      <div className="task-list">
        {tasks.map((task) => {
          const isDisabled =
            toggleLoading === task.id ||
            deleteLoading === task.id ||
            editLoading === task.id;

          return (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={onToggleComplete}
              onDelete={onDelete}
              onEdit={onEdit}
              disabled={isDisabled}
            />
          );
        })}
      </div>
    </div>
  );
}

export default TaskList;
