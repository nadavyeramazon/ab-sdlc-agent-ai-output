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

  // Show error but still render tasks if they exist (for rollback scenarios)
  const hasError = !!error;
  const hasTasks = tasks.length > 0;

  if (!hasTasks && !hasError) {
    return <div className="no-tasks">No tasks yet</div>;
  }

  return (
    <>
      {hasError && <div className="error">{error}</div>}
      {hasTasks ? (
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
      ) : (
        <div className="no-tasks">No tasks yet</div>
      )}
    </>
  );
}

export default TaskList;
