import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

describe('Delete All Tasks Feature', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();

    // Default mock for tasks endpoint
    global.fetch.mockImplementation((url) => {
      if (url.includes('/api/tasks')) {
        return Promise.resolve({
          ok: true,
          json: async () => ({ tasks: [] }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: async () => ({ message: 'Default response' }),
      });
    });
  });

  describe('Delete All Button Visibility', () => {
    it('should not display Delete All button when no tasks exist', async () => {
      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: [] }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete All button should not be visible
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should display Delete All button when tasks exist', async () => {
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
          completed: false,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Delete All button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });

    it('should display Delete All button even with single task', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Single Task',
          description: 'Only task',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Single Task')).toBeInTheDocument();
      });

      // Delete All button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });
  });

  describe('Confirmation Dialog Flow', () => {
    it('should show confirmation dialog when Delete All button is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation message should appear
      await waitFor(() => {
        expect(
          screen.getByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).toBeInTheDocument();
      });

      // Confirm and Cancel buttons should appear
      expect(
        screen.getByRole('button', { name: /yes, delete all/i })
      ).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: /cancel/i })
      ).toBeInTheDocument();
    });

    it('should cancel deletion when Cancel button is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation should appear
      await waitFor(() => {
        expect(
          screen.getByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).toBeInTheDocument();
      });

      // Click Cancel
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await user.click(cancelButton);

      // Confirmation dialog should disappear
      await waitFor(() => {
        expect(
          screen.queryByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).not.toBeInTheDocument();
      });

      // Delete All button should reappear
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Task should still be present
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  describe('Successful Deletion', () => {
    it('should delete all tasks when confirmed', async () => {
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
          completed: false,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
        },
        {
          id: '3',
          title: 'Task 3',
          description: 'Description 3',
          completed: true,
          created_at: '2024-01-03T00:00:00Z',
          updated_at: '2024-01-03T00:00:00Z',
        },
      ];

      let tasksDeleted = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          tasksDeleted = true;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: tasksDeleted ? [] : mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
        expect(screen.getByText('Task 3')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Wait for confirmation dialog
      await waitFor(() => {
        expect(
          screen.getByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).toBeInTheDocument();
      });

      // Confirm deletion
      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Verify API call was made
      await waitFor(() => {
        expect(tasksDeleted).toBe(true);
      });

      // All tasks should be removed
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 3')).not.toBeInTheDocument();
      });

      // Empty state should appear
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();

      // Delete All button should disappear
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should make DELETE request to correct endpoint', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let deleteCallMade = false;
      let deleteUrl = '';
      let deleteOptions = {};

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          deleteCallMade = true;
          deleteUrl = url;
          deleteOptions = options;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: deleteCallMade ? [] : mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Verify DELETE request was made to correct endpoint
      await waitFor(() => {
        expect(deleteCallMade).toBe(true);
        expect(deleteUrl).toContain('/api/tasks');
        expect(deleteOptions.method).toBe('DELETE');
      });
    });
  });

  describe('Loading States', () => {
    it('should disable buttons during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let deleteStarted = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          deleteStarted = true;
          return new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  status: 204,
                }),
              100
            )
          );
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      // Click confirm
      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Wait for deletion to start
      await waitFor(() => {
        expect(deleteStarted).toBe(true);
      });

      // Buttons should be disabled during deletion
      await waitFor(() => {
        const confirmBtn = screen.getByRole('button', { name: /deleting\.\.\./i });
        expect(confirmBtn).toBeDisabled();
      });

      // Wait for completion
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should show "Deleting..." text during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          return new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  status: 204,
                }),
              100
            )
          );
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // "Deleting..." should appear
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /deleting\.\.\./i })).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API error during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          return Promise.resolve({
            ok: false,
            status: 500,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Error message should appear
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(/HTTP error! status: 500/i);
      });

      // Tasks should still be present (deletion failed)
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should handle network error during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          return Promise.reject(new Error('Network connection failed'));
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Error message should appear
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(/Network connection failed/i);
      });

      // Tasks should still be present (deletion failed)
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  describe('UI State After Deletion', () => {
    it('should hide confirmation dialog after successful deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let tasksDeleted = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          tasksDeleted = true;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: tasksDeleted ? [] : mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Trigger deletion
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Confirmation dialog should disappear
      await waitFor(() => {
        expect(
          screen.queryByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: /yes, delete all/i })).not.toBeInTheDocument();
      });
    });

    it('should show empty state after deleting all tasks', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          title: 'Task 2',
          description: '',
          completed: false,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
        },
      ];

      let tasksDeleted = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          tasksDeleted = true;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: tasksDeleted ? [] : mockTasks }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Delete all tasks
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Empty state should appear
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // No tasks should be visible
      expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
    });
  });
});
