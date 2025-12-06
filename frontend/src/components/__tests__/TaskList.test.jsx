import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import TaskList from '../TaskList';

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: '1',
      title: 'Test Task 1',
      description: 'Description 1',
      completed: false,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
    {
      id: '2',
      title: 'Test Task 2',
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
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
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
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.queryByText('Test Task 1')).not.toBeInTheDocument();
      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    it('should display error when there are no tasks and error exists', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error="Failed to load tasks"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
      expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
    });

    it('should display error AND tasks when both exist', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="HTTP error! status: 500"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      // Error should be visible
      expect(screen.getByText('HTTP error! status: 500')).toBeInTheDocument();

      // Tasks should also be visible
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    });

    it('should display error message with proper styling', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error="Network error"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      const errorElement = screen.getByText('Network error');
      expect(errorElement).toHaveClass('error');
    });
  });

  describe('Empty State', () => {
    it('should display empty state message when no tasks exist', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });

    it('should not display empty state when tasks exist', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
    });

    it('should not display empty state when error exists', () => {
      render(
        <TaskList
          tasks={[]}
          loading={false}
          error="Failed to load"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
      expect(screen.getByText('Failed to load')).toBeInTheDocument();
    });
  });

  describe('Task Rendering', () => {
    it('should render all tasks when provided', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
      expect(screen.getByText('Description 1')).toBeInTheDocument();
      expect(screen.getByText('Description 2')).toBeInTheDocument();
    });

    it('should render tasks with correct completion status', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('○ Incomplete')).toBeInTheDocument();
      expect(screen.getByText('✓ Completed')).toBeInTheDocument();
    });

    it('should render task list with proper container', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      const taskList = document.querySelector('.task-list');
      expect(taskList).toBeInTheDocument();
      expect(taskList.children.length).toBe(2);
    });

    it('should pass disabled state to tasks during toggle operation', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading="1"
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      const checkboxes = screen.getAllByRole('checkbox');
      expect(checkboxes[0]).toBeDisabled();
      expect(checkboxes[1]).not.toBeDisabled();
    });

    it('should pass disabled state to tasks during delete operation', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading="1"
          editLoading={null}
          {...mockHandlers}
        />
      );

      const deleteButtons = screen.getAllByRole('button', {
        name: /delete task/i,
      });
      expect(deleteButtons[0]).toBeDisabled();
      expect(deleteButtons[1]).not.toBeDisabled();
    });

    it('should pass disabled state to tasks during edit operation', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading="1"
          {...mockHandlers}
        />
      );

      const editButtons = screen.getAllByRole('button', { name: /edit task/i });
      expect(editButtons[0]).toBeDisabled();
      expect(editButtons[1]).not.toBeDisabled();
    });
  });

  describe('Edge Cases', () => {
    it('should handle single task', () => {
      render(
        <TaskList
          tasks={[mockTasks[0]]}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument();
    });

    it('should handle tasks without descriptions', () => {
      const taskWithoutDesc = {
        id: '1',
        title: 'Task without description',
        description: '',
        completed: false,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };

      render(
        <TaskList
          tasks={[taskWithoutDesc]}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('Task without description')).toBeInTheDocument();
      const taskItem = screen
        .getByText('Task without description')
        .closest('.task-item');
      expect(taskItem.querySelector('.task-description')).not.toBeInTheDocument();
    });

    it('should prioritize loading over error display', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={true}
          error="Some error"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
      expect(screen.queryByText('Some error')).not.toBeInTheDocument();
    });

    it('should render error above task list when both exist', () => {
      const { container } = render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error="Operation failed"
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      const errorDiv = container.querySelector('.error');
      const taskListDiv = container.querySelector('.task-list');

      // Error should appear before task list in DOM
      expect(errorDiv).toBeInTheDocument();
      expect(taskListDiv).toBeInTheDocument();
      expect(
        errorDiv.compareDocumentPosition(taskListDiv) &
          Node.DOCUMENT_POSITION_FOLLOWING
      ).toBeTruthy();
    });
  });

  describe('Component Props Integration', () => {
    it('should pass all required props to TaskItem components', () => {
      render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      // Verify that TaskItem components have access to their handlers
      expect(screen.getAllByRole('checkbox')).toHaveLength(2);
      expect(screen.getAllByRole('button', { name: /delete task/i })).toHaveLength(
        2
      );
      expect(screen.getAllByRole('button', { name: /edit task/i })).toHaveLength(2);
    });

    it('should render unique keys for each task', () => {
      const { container } = render(
        <TaskList
          tasks={mockTasks}
          loading={false}
          error={null}
          toggleLoading={null}
          deleteLoading={null}
          editLoading={null}
          {...mockHandlers}
        />
      );

      const taskItems = container.querySelectorAll('.task-item');
      expect(taskItems).toHaveLength(2);
    });
  });
});
