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
      <div className="task-list">
        {tasks.map((task) => {
          const isDisabled =
            toggleLoading === task.id ||
            deleteLoading === task.id ||
            editLoading === task.id ||
            deleteAllLoading;

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
    </>
  );
}

export default TaskList;
