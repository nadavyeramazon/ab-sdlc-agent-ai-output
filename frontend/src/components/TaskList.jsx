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
}) {
  if (loading) {
    return <div className="loading">Loading tasks...</div>;
  }

  // If there's an error and no tasks, show only the error
  if (error && tasks.length === 0) {
    return <div className="error">{error}</div>;
  }

  // If no tasks and no error, show empty state
  if (tasks.length === 0) {
    return <div className="no-tasks">No tasks yet</div>;
  }

  // Render tasks list with optional error message above
  return (
    <>
      {error && <div className="error">{error}</div>}
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
    </>
  );
}

export default TaskList;
