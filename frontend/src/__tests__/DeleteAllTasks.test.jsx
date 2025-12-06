import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

describe('Delete All Tasks Feature', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();

    // Mock window.confirm
    global.confirm = vi.fn(() => true);

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

  afterEach(async () => {
    // Flush pending promises
    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });
    vi.restoreAllMocks();
  });

  describe('Delete All Button Rendering', () => {
    it('should not render delete all button when no tasks exist', async () => {
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

      const deleteAllButton = screen.queryByRole('button', {
        name: /delete all tasks/i,
      });
      expect(deleteAllButton).not.toBeInTheDocument();
    });

    it('should render delete all button when tasks exist', async () => {
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      expect(deleteAllButton).toBeInTheDocument();
      expect(deleteAllButton).not.toBeDisabled();
    });

    it('should render delete all button with trash icon', async () => {
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

      render(<App />);

      await waitFor(() => {
        const deleteAllButton = screen.getByRole('button', {
          name: /delete all tasks/i,
        });
        expect(deleteAllButton.textContent).toContain('🗑️');
      });
    });
  });

  describe('Delete All Confirmation Dialog', () => {
    it('should show confirmation dialog when delete all is clicked', async () => {
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      expect(global.confirm).toHaveBeenCalledWith(
        'Are you sure you want to delete all tasks? This action cannot be undone.'
      );
    });

    it('should not delete tasks if user cancels confirmation', async () => {
      global.confirm = vi.fn(() => false); // User clicks "Cancel"

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

      let deleteAllCalled = false;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          deleteAllCalled = true;
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: 1 }),
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Verify task is still displayed
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(deleteAllCalled).toBe(false);
    });
  });

  describe('Delete All Integration Flow', () => {
    it('should complete full delete all flow: button → confirm → API → empty state', async () => {
      let taskList = [
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

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          const count = taskList.length;
          taskList = [];
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: count }),
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

      // Wait for all tasks to load
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

      // Verify confirmation was shown
      expect(global.confirm).toHaveBeenCalled();

      // Wait for tasks to be deleted
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 3')).not.toBeInTheDocument();
      });

      // Verify empty state is shown
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();

      // Verify delete all button is no longer visible
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should delete all tasks even when some are completed', async () => {
      let taskList = [
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

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          taskList = [];
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: 2 }),
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
        expect(screen.getByText('Incomplete Task')).toBeInTheDocument();
        expect(screen.getByText('Completed Task')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });
  });

  describe('Delete All Loading States', () => {
    it('should show loading text during delete all operation', async () => {
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

      let resolveDelete;
      const deletePromise = new Promise((resolve) => {
        resolveDelete = resolve;
      });

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          return deletePromise.then(() => ({
            ok: true,
            json: async () => ({ success: true, deletedCount: 1 }),
          }));
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Start the delete operation but don't await it yet
      const clickPromise = user.click(deleteAllButton);

      // Wait for loading state to appear
      await waitFor(() => {
        const loadingButton = screen.queryByRole('button', {
          name: /deleting all/i,
        });
        expect(loadingButton).toBeInTheDocument();
        expect(loadingButton).toBeDisabled();
      });

      // Now resolve the delete operation
      act(() => {
        resolveDelete();
      });

      // Wait for the click to complete
      await clickPromise;

      // Wait for deletion to complete
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should disable delete all button during operation', async () => {
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

      let resolveDelete;
      const deletePromise = new Promise((resolve) => {
        resolveDelete = resolve;
      });

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          return deletePromise.then(() => ({
            ok: true,
            json: async () => ({ success: true, deletedCount: 1 }),
          }));
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Start the delete operation but don't await it yet
      const clickPromise = user.click(deleteAllButton);

      // Wait for button to be disabled during operation
      await waitFor(() => {
        const loadingButton = screen.queryByRole('button', {
          name: /deleting all/i,
        });
        expect(loadingButton).toBeInTheDocument();
        expect(loadingButton).toBeDisabled();
      });

      // Resolve the delete operation
      act(() => {
        resolveDelete();
      });

      // Wait for the click to complete
      await clickPromise;

      // Wait for completion
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });
  });

  describe('Delete All Error Handling', () => {
    it('should display error message when delete all fails', async () => {
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
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
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

      // Wait for initial task load
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Click the button and wait for all state updates
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Wait for error message to appear
      await waitFor(
        () => {
          expect(
            screen.getByText(/failed to delete all tasks/i)
          ).toBeInTheDocument();
        },
        { timeout: 3000 }
      );

      // Wait for tasks to be restored after rollback
      // The rollback happens in the catch block, so tasks should reappear
      await waitFor(
        () => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        },
        { timeout: 3000 }
      );
    });

    it('should auto-dismiss error message after 5 seconds', async () => {
      vi.useFakeTimers({ shouldAdvanceTime: true });

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
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
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

      const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
      render(<App />);

      // Wait for initial render with timer flush
      await act(async () => {
        await vi.runAllTimersAsync();
      });

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Click and handle state updates
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Error should be visible
      await waitFor(() => {
        expect(
          screen.getByText(/failed to delete all tasks/i)
        ).toBeInTheDocument();
      });

      // Advance timers by 5 seconds
      await act(async () => {
        await vi.advanceTimersByTimeAsync(5000);
      });

      // Error should be dismissed
      await waitFor(() => {
        expect(
          screen.queryByText(/failed to delete all tasks/i)
        ).not.toBeInTheDocument();
      });

      vi.useRealTimers();
    }, 10000); // Increase timeout for this test

    it('should handle network errors during delete all', async () => {
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
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          return Promise.reject(new Error('Network error'));
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Click the button and wait for all state updates
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Wait for error message to appear
      await waitFor(
        () => {
          expect(
            screen.getByText(/failed to delete all tasks/i)
          ).toBeInTheDocument();
        },
        { timeout: 3000 }
      );

      // Wait for task to be restored after rollback
      await waitFor(
        () => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        },
        { timeout: 3000 }
      );
    });
  });

  describe('Delete All Edge Cases', () => {
    it('should handle delete all when only one task exists', async () => {
      let taskList = [
        {
          id: '1',
          title: 'Only Task',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          taskList = [];
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: 1 }),
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
        expect(screen.getByText('Only Task')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should handle delete all with many tasks', async () => {
      const mockTasks = Array.from({ length: 10 }, (_, i) => ({
        id: `${i + 1}`,
        title: `Task ${i + 1}`,
        description: `Description ${i + 1}`,
        completed: i % 2 === 0,
        created_at: new Date(2024, 0, i + 1).toISOString(),
        updated_at: new Date(2024, 0, i + 1).toISOString(),
      }));

      let taskList = [...mockTasks];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          const count = taskList.length;
          taskList = [];
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: count }),
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
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 10')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      });
    });
  });

  describe('API Integration', () => {
    it('should call correct API endpoint with DELETE method', async () => {
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

      let apiCalled = false;
      let apiUrl = '';
      let apiMethod = '';

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/all') && options?.method === 'DELETE') {
          apiCalled = true;
          apiUrl = url;
          apiMethod = options.method;
          return Promise.resolve({
            ok: true,
            json: async () => ({ success: true, deletedCount: 1 }),
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

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(apiCalled).toBe(true);
      });

      expect(apiUrl).toContain('/api/tasks/all');
      expect(apiMethod).toBe('DELETE');
    });
  });
});
