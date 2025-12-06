import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import TaskList from '../TaskList';

describe('TaskList Component', () => {
  const mockTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  const defaultProps = {
    tasks: [],
    loading: false,
    error: null,
    onToggleComplete: vi.fn(),
    toggleLoading: null,
    onDelete: vi.fn(),
    deleteLoading: null,
    onEdit: vi.fn(),
    editLoading: null,
  };

  it('should render loading state', () => {
    render(<TaskList {...defaultProps} loading={true} />);
    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
  });

  it('should render empty state when no tasks', () => {
    render(<TaskList {...defaultProps} />);
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });

  it('should render task list when tasks exist', () => {
    render(<TaskList {...defaultProps} tasks={[mockTask]} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('should display error message alongside tasks', () => {
    const props = {
      ...defaultProps,
      tasks: [mockTask],
      error: 'Failed to delete task',
    };

    render(<TaskList {...props} />);

    // Both error and task should be visible
    expect(screen.getByText('Failed to delete task')).toBeInTheDocument();
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('should display error when there are no tasks', () => {
    const props = {
      ...defaultProps,
      error: 'Network error',
    };

    render(<TaskList {...props} />);

    // Error should be visible
    expect(screen.getByText('Network error')).toBeInTheDocument();
    // Empty state should also be visible
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });

  it('should prioritize loading state over error and tasks', () => {
    const props = {
      ...defaultProps,
      loading: true,
      error: 'Some error',
      tasks: [mockTask],
    };

    render(<TaskList {...props} />);

    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
    expect(screen.queryByText('Some error')).not.toBeInTheDocument();
    expect(screen.queryByText('Test Task')).not.toBeInTheDocument();
  });

  it('should display error with proper CSS class', () => {
    const props = {
      ...defaultProps,
      error: 'HTTP error! status: 500',
    };

    const { container } = render(<TaskList {...props} />);
    const errorElement = container.querySelector('.error');

    expect(errorElement).toBeInTheDocument();
    expect(errorElement.textContent).toBe('HTTP error! status: 500');
  });

  it('should not display error when error is null', () => {
    const props = {
      ...defaultProps,
      tasks: [mockTask],
      error: null,
    };

    const { container } = render(<TaskList {...props} />);

    expect(container.querySelector('.error')).not.toBeInTheDocument();
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('should render task list with proper CSS class', () => {
    const props = {
      ...defaultProps,
      tasks: [mockTask],
    };

    const { container } = render(<TaskList {...props} />);
    const taskListElement = container.querySelector('.task-list');

    expect(taskListElement).toBeInTheDocument();
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('should handle multiple tasks with error', () => {
    const tasks = [
      { ...mockTask, id: '1', title: 'Task 1' },
      { ...mockTask, id: '2', title: 'Task 2' },
      { ...mockTask, id: '3', title: 'Task 3' },
    ];

    const props = {
      ...defaultProps,
      tasks,
      error: 'Operation failed',
    };

    render(<TaskList {...props} />);

    // Error should be visible
    expect(screen.getByText('Operation failed')).toBeInTheDocument();

    // All tasks should be visible
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
    expect(screen.getByText('Task 3')).toBeInTheDocument();
  });
});
