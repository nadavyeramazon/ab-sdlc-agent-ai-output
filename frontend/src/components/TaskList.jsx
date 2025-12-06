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

  return (
    <>
      {error && <div className="error">{error}</div>}
      {tasks.length === 0 ? (
        <div className="no-tasks">No tasks yet</div>
      ) : (
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
      )}
    </>
  );
}

export default TaskList;
