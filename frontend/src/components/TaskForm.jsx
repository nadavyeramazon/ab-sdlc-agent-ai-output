import { useState, useEffect } from 'react';

function TaskForm({ onSubmit, onCancel, loading, error, initialData, isEditing }) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [validationError, setValidationError] = useState('');

  // Update form when initialData changes (for edit mode)
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || '');
      setDescription(initialData.description || '');
    } else if (!isEditing) {
      // Clear form when switching back to create mode
      setTitle('');
      setDescription('');
    }
  }, [initialData, isEditing]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Client-side validation
    if (!title.trim()) {
      setValidationError('Title cannot be empty');
      return;
    }

    setValidationError('');
    const success = await onSubmit({ title: title.trim(), description });

    // Clear form after successful submission (only for create mode)
    if (success && !isEditing) {
      setTitle('');
      setDescription('');
    }
  };

  const handleCancel = () => {
    setTitle('');
    setDescription('');
    setValidationError('');
    if (onCancel) {
      onCancel();
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="task-title">Title *</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          disabled={loading}
          className={validationError ? 'input-error' : ''}
        />
      </div>

      <div className="form-group">
        <label htmlFor="task-description">Description</label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description (optional)"
          disabled={loading}
          rows="3"
        />
      </div>

      {validationError && <div className="form-error">{validationError}</div>}

      {error && <div className="form-error">{error}</div>}

      <div className="form-actions">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading
            ? isEditing
              ? 'Updating...'
              : 'Creating...'
            : isEditing
              ? 'Update Task'
              : 'Create Task'}
        </button>
        {onCancel && (
          <button type="button" onClick={handleCancel} disabled={loading} className="btn-secondary">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default TaskForm;
