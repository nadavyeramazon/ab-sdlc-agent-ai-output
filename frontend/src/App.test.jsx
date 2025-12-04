import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import App from './App';

describe('Delete All Tasks Feature', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();

    // Mock fetch API
    global.fetch = vi.fn();

    // Mock window.confirm
    global.confirm = vi.fn();
  });

  describe('Delete All Button Rendering', () => {
    it('should not render Delete All button when there are no tasks', async () => {
      // Mock empty task list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: [] }),
      });

      render(<App />);

      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.queryByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete All button should not be visible
      expect(
        screen.queryByRole('button', { name: 'Delete all tasks' })
      ).not.toBeInTheDocument();
      expect(screen.queryByText(/Delete All Tasks/i)).not.toBeInTheDocument();
    });

    it('should render Delete All button when there are tasks', async () => {
      // Mock task list with one task
      const mockTasks = [
        {
          id: 1,
          title: 'Test Task',
          description: 'Test Description',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Delete All button should be visible
      expect(
        screen.getByRole('button', { name: 'Delete all tasks' })
      ).toBeInTheDocument();
    });

    it('should render Delete All button with trash icon emoji', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });
      expect(deleteAllButton).toHaveTextContent('🗑️ Delete All Tasks');
    });
  });

  describe('Delete All Confirmation', () => {
    it('should show confirmation dialog when Delete All is clicked', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      // Mock user canceling confirmation
      global.confirm.mockReturnValueOnce(false);

      await userEvent.click(deleteAllButton);

      // Confirmation should be shown
      expect(global.confirm).toHaveBeenCalledWith(
        'Are you sure you want to delete ALL tasks? This action cannot be undone.'
      );
    });

    it('should not delete tasks when user cancels confirmation', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      // Mock user canceling confirmation
      global.confirm.mockReturnValueOnce(false);

      await userEvent.click(deleteAllButton);

      // Task should still be visible
      expect(screen.getByText('Task 1')).toBeInTheDocument();

      // DELETE API should not have been called
      // Only the initial GET for tasks should have been called
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });
  });

  describe('Delete All Functionality', () => {
    it('should delete all tasks when user confirms', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          title: 'Task 2',
          description: '',
          completed: true,
          created_at: new Date().toISOString(),
        },
      ];

      // Mock initial fetch for tasks
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      // Mock user confirming deletion
      global.confirm.mockReturnValueOnce(true);

      // Mock DELETE all tasks API call
      global.fetch.mockResolvedValueOnce({
        ok: true,
      });

      await userEvent.click(deleteAllButton);

      // Wait for API call
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/tasks',
          { method: 'DELETE' }
        );
      });

      // Wait for tasks to be removed from UI
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
      });

      // Should show "No tasks yet" message
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });

    it('should show loading state while deleting all tasks', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValueOnce(true);

      // Mock DELETE with delay to test loading state
      global.fetch.mockImplementationOnce(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                }),
              100
            )
          )
      );

      await userEvent.click(deleteAllButton);

      // Should show loading text
      expect(screen.getByText('Deleting All...')).toBeInTheDocument();

      // Button should be disabled during loading
      expect(deleteAllButton).toBeDisabled();

      // Wait for deletion to complete
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      });
    });

    it('should disable Delete All button when tasks are loading', async () => {
      global.fetch.mockImplementationOnce(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  json: async () => ({ tasks: [] }),
                }),
              100
            )
          )
      );

      render(<App />);

      // Check if "Loading tasks..." is shown during initial load
      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });
  });

  describe('Delete All Error Handling', () => {
    it('should show error message when delete all fails', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValueOnce(true);

      // Mock DELETE failure
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      await userEvent.click(deleteAllButton);

      // Wait for error message
      await waitFor(() => {
        expect(
          screen.getByText(/HTTP error! status: 500/)
        ).toBeInTheDocument();
      });

      // Task should still be visible (not deleted)
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should show error message when delete all request throws', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValueOnce(true);

      // Mock network error
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      await userEvent.click(deleteAllButton);

      // Wait for error message
      await waitFor(() => {
        expect(screen.getByText(/Network error/)).toBeInTheDocument();
      });

      // Task should still be visible (not deleted)
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should clear error message after 5 seconds', async () => {
      vi.useFakeTimers();

      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValueOnce(true);

      // Mock DELETE failure
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      // Setup userEvent to work with fake timers
      const user = userEvent.setup({
        advanceTimers: vi.advanceTimersByTime,
      });

      await user.click(deleteAllButton);

      // Wait for error message
      await waitFor(() => {
        expect(
          screen.getByText(/HTTP error! status: 500/)
        ).toBeInTheDocument();
      });

      // Fast-forward time by 5 seconds wrapped in act
      await act(async () => {
        vi.advanceTimersByTime(5000);
      });

      // Error should be cleared
      await waitFor(() => {
        expect(
          screen.queryByText(/HTTP error! status: 500/)
        ).not.toBeInTheDocument();
      });

      vi.useRealTimers();
    });
  });

  describe('Delete All Button States', () => {
    it('should disable Delete All button when deleteAllLoading is true', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValueOnce(true);

      // Mock slow DELETE
      global.fetch.mockImplementationOnce(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                }),
              100
            )
          )
      );

      await userEvent.click(deleteAllButton);

      // Button should be disabled during deletion
      await waitFor(() => {
        expect(deleteAllButton).toBeDisabled();
      });
    });

    it('should not allow clicking Delete All multiple times', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });

      global.confirm.mockReturnValue(true);

      // Mock slow DELETE
      global.fetch.mockImplementation(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                }),
              100
            )
          )
      );

      // Try to click multiple times
      await userEvent.click(deleteAllButton);
      await userEvent.click(deleteAllButton);
      await userEvent.click(deleteAllButton);

      // Only one DELETE request should be made (plus the initial GET)
      await waitFor(() => {
        const deleteCalls = global.fetch.mock.calls.filter(
          (call) => call[1]?.method === 'DELETE'
        );
        expect(deleteCalls).toHaveLength(1);
      });
    });
  });

  describe('Integration with Task List', () => {
    it('should remove Delete All button after all tasks are deleted', async () => {
      const mockTasks = [
        {
          id: 1,
          title: 'Task 1',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ];

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: mockTasks }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Delete All button should be visible
      let deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });
      expect(deleteAllButton).toBeInTheDocument();

      global.confirm.mockReturnValueOnce(true);

      global.fetch.mockResolvedValueOnce({
        ok: true,
      });

      await userEvent.click(deleteAllButton);

      // Wait for tasks to be deleted
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      });

      // Delete All button should be gone
      expect(
        screen.queryByRole('button', { name: 'Delete all tasks' })
      ).not.toBeInTheDocument();

      // Should show "No tasks yet" message
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });

    it('should work correctly after creating and deleting all tasks', async () => {
      // Start with empty task list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ tasks: [] }),
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Create a new task
      const titleInput = screen.getByLabelText('Title *');
      await userEvent.type(titleInput, 'New Task');

      // Mock POST request
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          title: 'New Task',
          description: '',
          completed: false,
          created_at: new Date().toISOString(),
        }),
      });

      const createButton = screen.getByRole('button', { name: /Create Task/ });
      await userEvent.click(createButton);

      // Wait for task to be created
      await waitFor(() => {
        expect(screen.getByText('New Task')).toBeInTheDocument();
      });

      // Delete All button should now be visible
      const deleteAllButton = screen.getByRole('button', {
        name: 'Delete all tasks',
      });
      expect(deleteAllButton).toBeInTheDocument();

      global.confirm.mockReturnValueOnce(true);

      // Mock DELETE all
      global.fetch.mockResolvedValueOnce({
        ok: true,
      });

      await userEvent.click(deleteAllButton);

      // Wait for task to be deleted
      await waitFor(() => {
        expect(screen.queryByText('New Task')).not.toBeInTheDocument();
      });

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });
  });
});
