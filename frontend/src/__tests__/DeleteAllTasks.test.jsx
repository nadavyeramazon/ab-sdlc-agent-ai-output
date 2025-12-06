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

    // Mock fetch for tasks endpoint by default
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
    it('should not show delete all button when no tasks exist', async () => {
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

      // Delete all button should not be visible
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should show delete all button when tasks exist', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Delete all button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });

    it('should show delete all button with multiple tasks', async () => {
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
        expect(screen.getByText('Task 2')).toBeInTheDocument();
        expect(screen.getByText('Task 3')).toBeInTheDocument();
      });

      // Delete all button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });
  });

  describe('Confirmation Dialog', () => {
    it('should show confirmation dialog when delete all button is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation message should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      // Confirmation buttons should appear
      expect(
        screen.getByRole('button', { name: /yes, delete all/i })
      ).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: /cancel/i })
      ).toBeInTheDocument();
    });

    it('should hide initial delete all button when confirmation is shown', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Initial button should be hidden
      await waitFor(() => {
        expect(
          screen.queryByRole('button', { name: /^delete all tasks$/i })
        ).not.toBeInTheDocument();
      });
    });
  });

  describe('Cancel Deletion', () => {
    it('should hide confirmation dialog when cancel is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      // Click cancel
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await user.click(cancelButton);

      // Confirmation should disappear
      await waitFor(() => {
        expect(
          screen.queryByText(/are you sure you want to delete all tasks/i)
        ).not.toBeInTheDocument();
      });

      // Original button should be back
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Tasks should still exist
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should not call API when cancel is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let deleteAllCalled = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          deleteAllCalled = true;
          return Promise.resolve({
            ok: true,
            status: 204,
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      // Click cancel
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await user.click(cancelButton);

      // Wait a bit to ensure no API call is made
      await new Promise((resolve) => setTimeout(resolve, 100));

      // API should not have been called
      expect(deleteAllCalled).toBe(false);
    });
  });

  describe('Delete All Functionality', () => {
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
      ];

      let currentTasks = [...mockTasks];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          currentTasks = [];
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: currentTasks }),
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      // Click confirm
      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // All tasks should be removed
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete all button should be hidden (no tasks)
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should call DELETE /api/tasks endpoint', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let deleteAllCalled = false;
      let deleteAllUrl = '';
      let deleteAllMethod = '';

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          deleteAllCalled = true;
          deleteAllUrl = url;
          deleteAllMethod = options.method;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: deleteAllCalled ? [] : mockTasks }),
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

      // Click delete all and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Verify API was called correctly
      await waitFor(() => {
        expect(deleteAllCalled).toBe(true);
        expect(deleteAllUrl).toContain('/api/tasks');
        expect(deleteAllMethod).toBe('DELETE');
      });
    });

    it('should work with mix of completed and incomplete tasks', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Incomplete Task',
          description: 'Not done',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          title: 'Completed Task',
          description: 'Done',
          completed: true,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
        },
      ];

      let currentTasks = [...mockTasks];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          currentTasks = [];
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: currentTasks }),
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
        expect(screen.getByText('Incomplete Task')).toBeInTheDocument();
        expect(screen.getByText('Completed Task')).toBeInTheDocument();
      });

      // Delete all
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Both tasks should be removed
      await waitFor(() => {
        expect(screen.queryByText('Incomplete Task')).not.toBeInTheDocument();
        expect(screen.queryByText('Completed Task')).not.toBeInTheDocument();
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });
  });

  describe('Loading States', () => {
    it('should show loading text on confirm button during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Should show loading text
      expect(screen.getByText('Deleting...')).toBeInTheDocument();

      // Wait for deletion to complete
      await waitFor(
        () => {
          expect(screen.queryByText('Deleting...')).not.toBeInTheDocument();
        },
        { timeout: 3000 }
      );
    });

    it('should disable buttons during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Buttons should be disabled
      await waitFor(() => {
        const deletingButton = screen.getByText('Deleting...');
        expect(deletingButton).toBeDisabled();

        const cancelButton = screen.getByRole('button', { name: /cancel/i });
        expect(cancelButton).toBeDisabled();
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors during delete all', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Should show error message
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(/HTTP error! status: 500/i);
      });

      // Task should still exist
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should handle network errors during delete all', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
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

      // Click delete all and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Should show error message
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(/Network connection failed/i);
      });

      // Task should still exist
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });
});
