import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import TaskList from '../TaskList';

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
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
    },
  ];

  const mockHandlers = {
    onToggleComplete: vi.fn(),
    onDelete: vi.fn(),
    onEdit: vi.fn(),
  };

  describe('Loading State', () => {
    it('should display loading message when loading is true', () => {
      render(
        <TaskList
          tasks={[]}
          loading={true}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
    });

    it('should not display tasks when loading', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={true}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('should display error message when error is present', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error="Failed to load tasks"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
    });

    it('should display both error and tasks when error occurs after rollback', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="HTTP error! status: 500"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      // Both error message and tasks should be visible
      expect(screen.getByText('HTTP error! status: 500')).toBeInTheDocument();
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });

    it('should display error and empty state when error occurs with no tasks', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error="HTTP error! status: 500"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('HTTP error! status: 500')).toBeInTheDocument();
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('should display empty state when no tasks exist', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });

    it('should not display task list when no tasks exist', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(
        document.querySelector('.task-list')
      ).not.toBeInTheDocument();
    });
  });

  describe('Task Rendering', () => {
    it('should render all tasks when tasks exist', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });

    it('should not display empty state when tasks exist', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
    });

    it('should render correct number of task items', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      const taskItems = document.querySelectorAll('.task-item');
      expect(taskItems).toHaveLength(2);
    });
  });

  describe('Priority States', () => {
    it('should prioritize loading state over error state', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={true}
          error="Some error"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
      expect(screen.queryByText('Some error')).not.toBeInTheDocument();
      expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
    });

    it('should show error with tasks when both are present', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="Operation failed"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      // Both should be visible
      expect(screen.getByText('Operation failed')).toBeInTheDocument();
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  describe('Optimistic Update Rollback Scenario', () => {
    it('should correctly display rolled-back tasks after failed delete all', () => {
      // This simulates what happens after a delete all operation fails:
      // 1. Tasks are optimistically cleared (tasks = [])
      // 2. API call fails
      // 3. Tasks are rolled back (tasks = originalTasks)
      // 4. Error is set
      // Result: Both error and tasks should be visible

      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="HTTP error! status: 500"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      // Error should be displayed
      const errorElement = screen.getByText('HTTP error! status: 500');
      expect(errorElement).toBeInTheDocument();
      expect(errorElement).toHaveClass('error');

      // Tasks should be visible after rollback
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();

      // Task list container should exist
      const taskList = document.querySelector('.task-list');
      expect(taskList).toBeInTheDocument();
    });

    it('should render error above task list in DOM order', () => {
      const { container } = render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="HTTP error! status: 500"
          {...mockHandlers}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={false}
        />
      );

      const children = Array.from(container.firstChild.children);
      expect(children[0]).toHaveClass('error');
      expect(children[1]).toHaveClass('task-list');
    });
  });
});
