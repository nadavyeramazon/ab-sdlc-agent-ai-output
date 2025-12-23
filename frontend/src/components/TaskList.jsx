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

  // Show error message if present, but continue to render tasks below
  const errorDisplay = error ? <div className="error">{error}</div> : null;

  if (tasks.length === 0) {
    return (
      <>
        {errorDisplay}
        <div className="no-tasks">No tasks yet</div>
      </>
    );
  }

  return (
    <>
      {errorDisplay}
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
