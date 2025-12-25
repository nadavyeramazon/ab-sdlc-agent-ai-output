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
  });

  describe('Delete All Button Visibility', () => {
    it('should not display delete all button when task list is empty', async () => {
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

    it('should display delete all button when tasks exist', async () => {
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

      // Delete all button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });

    it('should hide delete all button after all tasks are deleted individually', async () => {
      let taskList = [
        {
          id: '1',
          title: 'Last Task',
          description: 'This is the last one',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
          taskList = [];
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: taskList }),
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
        expect(screen.getByText('Last Task')).toBeInTheDocument();
      });

      // Delete all button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Delete the task
      const deleteButton = screen.getByRole('button', {
        name: /delete task "last task"/i,
      });
      await user.click(deleteButton);

      // Wait for task to be deleted
      await waitFor(() => {
        expect(screen.queryByText('Last Task')).not.toBeInTheDocument();
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete all button should be hidden
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });
  });

  describe('Delete All Confirmation Dialog', () => {
    it('should show confirmation dialog when delete all button is clicked', async () => {
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

      // Confirmation dialog should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 2 tasks/i)
        ).toBeInTheDocument();
      });

      // Should have cancel and confirm buttons
      expect(
        screen.getByRole('button', { name: /^cancel$/i })
      ).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: /delete all/i })
      ).toBeInTheDocument();
    });

    it('should display correct task count in confirmation message (singular)', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Only Task',
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
        expect(screen.getByText('Only Task')).toBeInTheDocument();
      });

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Should use singular "task"
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });
    });

    it('should display correct task count in confirmation message (plural)', async () => {
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
        {
          id: '3',
          title: 'Task 3',
          description: '',
          completed: false,
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

      // Should use plural "tasks"
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 3 tasks\?/i)
        ).toBeInTheDocument();
      });
    });

    it('should hide delete all button when confirmation dialog is shown', async () => {
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation dialog should appear and delete all button should be hidden
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      // Original delete all button should not be in the document
      expect(
        screen.queryByRole('button', { name: /^delete all tasks$/i })
      ).not.toBeInTheDocument();
    });

    it('should close confirmation dialog when cancel is clicked', async () => {
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation dialog should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      // Click cancel
      const cancelButton = screen.getByRole('button', { name: /^cancel$/i });
      await user.click(cancelButton);

      // Confirmation dialog should disappear
      await waitFor(() => {
        expect(
          screen.queryByText(/are you sure you want to delete all 1 task\?/i)
        ).not.toBeInTheDocument();
      });

      // Delete all button should reappear
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Tasks should still be present
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  describe('Delete All Execution', () => {
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
          completed: false,
          created_at: '2024-01-03T00:00:00Z',
          updated_at: '2024-01-03T00:00:00Z',
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
        expect(screen.getByText('Task 3')).toBeInTheDocument();
      });

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation dialog should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 3 tasks\?/i)
        ).toBeInTheDocument();
      });

      // Click confirm
      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // All tasks should be deleted
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 3')).not.toBeInTheDocument();
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete all button should be hidden
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();

      // Verify API was called correctly
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tasks'),
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });

    it('should show loading state during delete all operation', async () => {
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // Should show loading text
      await waitFor(() => {
        expect(screen.getByText('Deleting...')).toBeInTheDocument();
      });

      // Wait for operation to complete
      await waitFor(() => {
        expect(screen.queryByText('Deleting...')).not.toBeInTheDocument();
      });
    });

    it('should disable buttons during delete all operation', async () => {
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // Buttons should be disabled during operation
      await waitFor(() => {
        const deletingButton = screen.getByRole('button', {
          name: /deleting.../i,
        });
        expect(deletingButton).toBeDisabled();

        const cancelButton = screen.getByRole('button', { name: /^cancel$/i });
        expect(cancelButton).toBeDisabled();
      });

      // Wait for operation to complete
      await waitFor(() => {
        expect(screen.queryByText('Deleting...')).not.toBeInTheDocument();
      });
    });

    it('should handle API error during delete all', async () => {
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
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 2 tasks\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // Should display error message
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(/HTTP error! status: 500/i);
      });

      // Tasks should still be present (no optimistic update on error)
      // Wrap in waitFor to handle async rendering
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Confirmation dialog should remain open
      expect(
        screen.getByText(/are you sure you want to delete all 2 tasks\?/i)
      ).toBeInTheDocument();
    });

    it('should handle network error during delete all', async () => {
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // Should display network error
      await waitFor(() => {
        const taskListSection = document.querySelector('.task-list-section');
        expect(taskListSection.textContent).toMatch(
          /Network connection failed/i
        );
      });

      // Task should still be present
      // Wrap in waitFor to handle async rendering
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });
    });
  });

  describe('Delete All with Mixed Task States', () => {
    it('should delete all tasks including completed and incomplete', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Incomplete Task',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          title: 'Completed Task',
          description: '',
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 2 tasks\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      // All tasks should be deleted
      await waitFor(() => {
        expect(screen.queryByText('Incomplete Task')).not.toBeInTheDocument();
        expect(screen.queryByText('Completed Task')).not.toBeInTheDocument();
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });
  });

  describe('Delete All Integration with Other Features', () => {
    it('should not interfere with task creation after delete all', async () => {
      const initialTasks = [
        {
          id: '1',
          title: 'Task to Delete',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      let currentTasks = [...initialTasks];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          currentTasks = [];
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks') && options?.method === 'POST') {
          const body = JSON.parse(options.body);
          const newTask = {
            id: '2',
            title: body.title,
            description: body.description || '',
            completed: false,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
          currentTasks = [newTask, ...currentTasks];
          return Promise.resolve({
            ok: true,
            status: 201,
            json: async () => newTask,
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
        expect(screen.getByText('Task to Delete')).toBeInTheDocument();
      });

      // Delete all tasks
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all 1 task\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', { name: /delete all/i });
      await user.click(confirmButton);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Create a new task
      const titleInput = screen.getByLabelText(/title/i);
      await user.type(titleInput, 'New Task After Delete All');

      const createButton = screen.getByRole('button', {
        name: /create task/i,
      });
      await user.click(createButton);

      // New task should appear
      await waitFor(() => {
        expect(
          screen.getByText('New Task After Delete All')
        ).toBeInTheDocument();
        expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
      });

      // Delete all button should reappear
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });
  });
});
