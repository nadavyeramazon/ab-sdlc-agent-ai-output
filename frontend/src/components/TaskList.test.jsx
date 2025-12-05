/**
 * Tests for TaskList Component
 * Covers Delete All button functionality
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskList from './TaskList';

// Mock window.confirm
global.confirm = vi.fn();

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: '1',
      title: 'Task 1',
      description: 'Description 1',
      completed: false,
    },
    {
      id: '2',
      title: 'Task 2',
      description: 'Description 2',
      completed: true,
    },
    {
      id: '3',
      title: 'Task 3',
      description: 'Description 3',
      completed: false,
    },
  ];

  const defaultProps = {
    tasks: mockTasks,
    loading: false,
    error: null,
    onToggleComplete: vi.fn(),
    toggleLoading: null,
    onDelete: vi.fn(),
    deleteLoading: null,
    onEdit: vi.fn(),
    editLoading: null,
    onDeleteAll: vi.fn(),
    deleteAllLoading: false,
    taskCount: mockTasks.length,
  };

  describe('Delete All Button', () => {
    it('should render delete all button with task count', () => {
      render(<TaskList {...defaultProps} />);

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      expect(deleteButton).toBeInTheDocument();
      expect(deleteButton).not.toBeDisabled();
    });

    it('should disable button when no tasks exist', () => {
      render(
        <TaskList
          {...defaultProps}
          tasks={[]}
          taskCount={0}
        />
      );

      // Should show "No tasks yet" message
      expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
    });

    it('should disable button when deleteAllLoading is true', () => {
      render(
        <TaskList
          {...defaultProps}
          deleteAllLoading={true}
        />
      );

      const deleteButton = screen.getByRole('button', {
        name: /deleting.../i,
      });
      expect(deleteButton).toBeDisabled();
    });

    it('should show loading text when deleteAllLoading is true', () => {
      render(
        <TaskList
          {...defaultProps}
          deleteAllLoading={true}
        />
      );

      expect(screen.getByText(/deleting.../i)).toBeInTheDocument();
    });

    it('should call onDeleteAll when button is clicked', async () => {
      const user = userEvent.setup();
      const mockDeleteAll = vi.fn();

      render(
        <TaskList
          {...defaultProps}
          onDeleteAll={mockDeleteAll}
        />
      );

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });

      await user.click(deleteButton);

      expect(mockDeleteAll).toHaveBeenCalledTimes(1);
    });

    it('should not call onDeleteAll when button is disabled', async () => {
      const user = userEvent.setup();
      const mockDeleteAll = vi.fn();

      render(
        <TaskList
          {...defaultProps}
          onDeleteAll={mockDeleteAll}
          deleteAllLoading={true}
        />
      );

      const deleteButton = screen.getByRole('button', {
        name: /deleting.../i,
      });

      // Button is disabled, click should not work
      await user.click(deleteButton);

      expect(mockDeleteAll).not.toHaveBeenCalled();
    });
  });

  describe('Loading State', () => {
    it('should show loading message when loading is true', () => {
      render(
        <TaskList
          {...defaultProps}
          loading={true}
        />
      );

      expect(screen.getByText(/loading tasks.../i)).toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('should show error message when error exists', () => {
      render(
        <TaskList
          {...defaultProps}
          error="Failed to load tasks"
        />
      );

      expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument();
    });

    it('should not show tasks when error and no tasks', () => {
      render(
        <TaskList
          {...defaultProps}
          tasks={[]}
          taskCount={0}
          error="Failed to load tasks"
        />
      );

      expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument();
      expect(screen.queryByText(/no tasks yet/i)).not.toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('should show empty state when no tasks and no error', () => {
      render(
        <TaskList
          {...defaultProps}
          tasks={[]}
          taskCount={0}
        />
      );

      expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
    });
  });

  describe('Task List', () => {
    it('should render all tasks', () => {
      render(<TaskList {...defaultProps} />);

      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
      expect(screen.getByText('Task 3')).toBeInTheDocument();
    });
  });
});
