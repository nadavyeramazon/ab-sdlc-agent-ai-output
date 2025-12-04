function TaskItem({ task, onToggle, onDelete, onEdit, disabled }) {
  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      <div className="task-header">
        <div className="task-header-left">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task.id, task.completed)}
            disabled={disabled}
            className="task-checkbox"
            aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          />
          <h3 className={task.completed ? 'task-title completed' : 'task-title'}>
            {task.title}
          </h3>
        </div>
        <div className="task-actions">
          <span className="task-status">{task.completed ? '✓ Completed' : '○ Incomplete'}</span>
          <button
            onClick={() => onEdit(task)}
            disabled={disabled}
            className="btn-edit"
            aria-label={`Edit task "${task.title}"`}
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            disabled={disabled}
            className="btn-delete"
            aria-label={`Delete task "${task.title}"`}
          >
            Delete
          </button>
        </div>
      </div>
      {task.description && <p className="task-description">{task.description}</p>}
      <div className="task-footer">
        <span className="task-date">
          Created: {new Date(task.created_at).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
}

export default TaskItem;
