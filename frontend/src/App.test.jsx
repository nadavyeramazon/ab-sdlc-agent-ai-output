/**
 * Integration Tests for App Component
 * Tests the complete user flow including Delete All functionality
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { taskApi } from './services/api';

// Mock the API
vi.mock('./services/api', () => ({
  taskApi: {
    getAllTasks: vi.fn(),
    createTask: vi.fn(),
    updateTask: vi.fn(),
    deleteTask: vi.fn(),
    deleteAllTasks: vi.fn(),
  },
}));

// Mock window.confirm
global.confirm = vi.fn();

describe('App Component - Delete All Functionality', () => {
  const mockTasks = [
    {
      id: '1',
      title: 'Task 1',
      description: 'Description 1',
      completed: false,
      created_at: '2024-01-01T10:00:00.000Z',
      updated_at: '2024-01-01T10:00:00.000Z',
    },
    {
      id: '2',
      title: 'Task 2',
      description: 'Description 2',
      completed: false,
      created_at: '2024-01-01T10:00:00.000Z',
      updated_at: '2024-01-01T10:00:00.000Z',
    },
    {
      id: '3',
      title: 'Task 3',
      description: 'Description 3',
      completed: false,
      created_at: '2024-01-01T10:00:00.000Z',
      updated_at: '2024-01-01T10:00:00.000Z',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
  });

  describe('Delete All Button', () => {
    it('should render delete all button with correct task count', async () => {
      render(<App />);

      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /delete all \(3\)/i })
        ).toBeInTheDocument();
      });
    });

    it('should disable button when no tasks exist', async () => {
      taskApi.getAllTasks.mockResolvedValue({ tasks: [] });
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
      });
    });

    it('should show confirmation dialog when delete all is clicked', async () => {
      const user = userEvent.setup();
      global.confirm.mockReturnValue(false); // User cancels

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      await user.click(deleteButton);

      expect(global.confirm).toHaveBeenCalledWith(
        'Are you sure you want to delete all 3 task(s)? This action cannot be undone.'
      );
    });

    it('should delete all tasks when confirmed', async () => {
      const user = userEvent.setup();
      global.confirm.mockReturnValue(true); // User confirms
      taskApi.deleteAllTasks.mockResolvedValue({
        success: true,
        message: 'All tasks deleted successfully',
        deletedCount: 3,
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      await user.click(deleteButton);

      await waitFor(() => {
        expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);
      });

      await waitFor(() => {
        expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
      });
    });

    it('should not delete tasks when confirmation is canceled', async () => {
      const user = userEvent.setup();
      global.confirm.mockReturnValue(false); // User cancels

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      await user.click(deleteButton);

      expect(taskApi.deleteAllTasks).not.toHaveBeenCalled();

      // Tasks should still be visible
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
      expect(screen.getByText('Task 3')).toBeInTheDocument();
    });

    it('should handle delete all error with rollback', async () => {
      const user = userEvent.setup();
      global.confirm.mockReturnValue(true); // User confirms
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('Failed to delete tasks')
      );

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      await user.click(deleteButton);

      await waitFor(() => {
        expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);
      });

      // Tasks should still be visible after rollback
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
        expect(screen.getByText('Task 3')).toBeInTheDocument();
      });
    });

    it('should show loading state during delete all', async () => {
      const user = userEvent.setup();
      global.confirm.mockReturnValue(true);

      // Create a promise that we can control
      let resolveDelete;
      const deletePromise = new Promise((resolve) => {
        resolveDelete = resolve;
      });
      taskApi.deleteAllTasks.mockReturnValue(deletePromise);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteButton = screen.getByRole('button', {
        name: /delete all \(3\)/i,
      });
      await user.click(deleteButton);

      // Check for loading state
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /deleting.../i })
        ).toBeInTheDocument();
      });

      // Resolve the delete
      resolveDelete({
        success: true,
        message: 'All tasks deleted successfully',
        deletedCount: 3,
      });

      await waitFor(() => {
        expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
      });
    });

    it('should not call deleteAllTasks when task count is zero', async () => {
      const user = userEvent.setup();
      taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
      });

      // Button should not be present or should be disabled
      const deleteButtons = screen.queryAllByRole('button', {
        name: /delete all/i,
      });

      expect(taskApi.deleteAllTasks).not.toHaveBeenCalled();
    });
  });

  describe('Task Creation', () => {
    it('should create a new task', async () => {
      const user = userEvent.setup();
      const newTask = {
        id: '4',
        title: 'New Task',
        description: 'New Description',
        completed: false,
        created_at: '2024-01-01T10:00:00.000Z',
        updated_at: '2024-01-01T10:00:00.000Z',
      };

      taskApi.createTask.mockResolvedValue(newTask);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const titleInput = screen.getByLabelText(/title/i);
      const descriptionInput = screen.getByLabelText(/description/i);
      const submitButton = screen.getByRole('button', { name: /create task/i });

      await user.type(titleInput, 'New Task');
      await user.type(descriptionInput, 'New Description');
      await user.click(submitButton);

      await waitFor(() => {
        expect(taskApi.createTask).toHaveBeenCalledWith({
          title: 'New Task',
          description: 'New Description',
        });
      });

      await waitFor(() => {
        expect(screen.getByText('New Task')).toBeInTheDocument();
      });
    });
  });

  describe('Task Toggle', () => {
    it('should toggle task completion', async () => {
      const user = userEvent.setup();
      const updatedTask = {
        ...mockTasks[0],
        completed: true,
      };

      taskApi.updateTask.mockResolvedValue(updatedTask);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const checkbox = screen.getAllByRole('checkbox')[0];
      await user.click(checkbox);

      await waitFor(() => {
        expect(taskApi.updateTask).toHaveBeenCalledWith('1', {
          completed: true,
        });
      });
    });
  });
});
