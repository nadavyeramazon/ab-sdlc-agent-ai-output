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

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (tasks.length === 0) {
    return <div className="no-tasks">No tasks yet</div>;
  }

  return (
    <div>
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
