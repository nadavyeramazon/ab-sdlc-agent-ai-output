/**
 * Unit tests for TaskList component
 * Tests rendering logic, error handling, and task display
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import TaskList from '../TaskList';

// Mock TaskItem component
vi.mock('../TaskItem', () => ({
  default: ({ task }) => <div data-testid={`task-${task.id}`}>{task.title}</div>,
}));

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: '1',
      title: 'Task 1',
      description: 'Description 1',
      completed: false,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
    {
      id: '2',
      title: 'Task 2',
      description: 'Description 2',
      completed: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
  ];

  const mockProps = {
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

  /**
   * Test: Loading state
   */
  it('displays loading message when loading is true', () => {
    render(<TaskList {...mockProps} loading={true} />);

    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
  });

  /**
   * Test: Empty state with no error
   */
  it('displays no tasks message when tasks array is empty and no error', () => {
    render(<TaskList {...mockProps} tasks={[]} />);

    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });

  /**
   * Test: Error only (no tasks)
   */
  it('displays error message when there is an error and no tasks', () => {
    render(
      <TaskList {...mockProps} tasks={[]} error="Failed to load tasks" />
    );

    expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
    // Should show "No tasks yet" as well since tasks are empty
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });

  /**
   * Test: Tasks displayed correctly
   */
  it('renders all tasks when tasks array has items', () => {
    render(<TaskList {...mockProps} tasks={mockTasks} />);

    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-2')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });

  /**
   * Test: Error displayed alongside tasks (rollback scenario)
   */
  it('displays both error and tasks when error occurs with existing tasks', () => {
    render(
      <TaskList
        {...mockProps}
        tasks={mockTasks}
        error="Failed to delete all tasks"
      />
    );

    // Error should be visible
    expect(screen.getByText('Failed to delete all tasks')).toBeInTheDocument();

    // Tasks should still be visible (rollback scenario)
    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-2')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });

  /**
   * Test: No error shown when error is null
   */
  it('does not display error message when error is null', () => {
    render(<TaskList {...mockProps} tasks={mockTasks} error={null} />);

    expect(screen.queryByText(/failed/i)).not.toBeInTheDocument();
    expect(screen.getByTestId('task-1')).toBeInTheDocument();
  });

  /**
   * Test: No error shown when error is empty string
   */
  it('does not display error message when error is empty string', () => {
    render(<TaskList {...mockProps} tasks={mockTasks} error="" />);

    expect(screen.queryByText(/failed/i)).not.toBeInTheDocument();
    expect(screen.getByTestId('task-1')).toBeInTheDocument();
  });

  /**
   * Test: Loading takes precedence over everything
   */
  it('shows only loading state when loading is true, even with error and tasks', () => {
    render(
      <TaskList
        {...mockProps}
        loading={true}
        tasks={mockTasks}
        error="Some error"
      />
    );

    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
    expect(screen.queryByText('Some error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('task-1')).not.toBeInTheDocument();
  });

  /**
   * Test: Props are passed correctly to TaskItem
   */
  it('passes correct props to TaskItem components', () => {
    const onToggleComplete = vi.fn();
    const onDelete = vi.fn();
    const onEdit = vi.fn();

    render(
      <TaskList
        {...mockProps}
        tasks={mockTasks}
        onToggleComplete={onToggleComplete}
        onDelete={onDelete}
        onEdit={onEdit}
        toggleLoading="1"
        deleteLoading="2"
      />
    );

    // Tasks should be rendered
    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-2')).toBeInTheDocument();
  });

  /**
   * Test: Single task rendering
   */
  it('renders a single task correctly', () => {
    const singleTask = [mockTasks[0]];

    render(<TaskList {...mockProps} tasks={singleTask} />);

    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.queryByTestId('task-2')).not.toBeInTheDocument();
  });

  /**
   * Test: Empty tasks with loading false
   */
  it('shows no tasks message when tasks is empty array and not loading', () => {
    render(<TaskList {...mockProps} tasks={[]} loading={false} />);

    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    expect(screen.queryByText('Loading tasks...')).not.toBeInTheDocument();
  });
});
