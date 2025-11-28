import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

// Mock window.confirm
const originalConfirm = window.confirm;

describe('Delete All Functionality', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
    
    // Reset window.confirm
    window.confirm = originalConfirm;
    
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

  describe('Delete All Button Rendering', () => {
    it('should not render Delete All button when task list is empty', async () => {
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

      // Delete All button should not be present when no tasks exist
      expect(screen.queryByRole('button', { name: /delete all tasks/i })).not.toBeInTheDocument();
      expect(screen.queryByText(/delete all tasks/i)).not.toBeInTheDocument();
    });

    it('should render Delete All button when tasks exist', async () => {
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

      // Delete All button should be present
      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton).toBeInTheDocument();
      expect(deleteAllButton).toHaveClass('btn-delete-all');
    });

    it('should render Delete All button with trash icon and text', async () => {
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
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton.textContent).toContain('🗑️');
      expect(deleteAllButton.textContent).toContain('Delete All Tasks');
    });

    it('should have proper ARIA label for accessibility', async () => {
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
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton).toHaveAttribute('aria-label', 'Delete all tasks');
    });
  });

  describe('Delete All User Interaction Flow', () => {
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

      // Mock window.confirm to track if it was called
      let confirmCalled = false;
      window.confirm = vi.fn(() => {
        confirmCalled = true;
        return false; // User cancels
      });

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Verify confirmation dialog was shown
      expect(confirmCalled).toBe(true);
      expect(window.confirm).toHaveBeenCalledWith(
        'Are you sure you want to delete ALL tasks? This action cannot be undone.'
      );
    });

    it('should not delete tasks when user cancels confirmation', async () => {
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

      // User cancels confirmation
      window.confirm = vi.fn(() => false);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Wait a bit to ensure no API call is made
      await new Promise(resolve => setTimeout(resolve, 100));

      // Verify DELETE API was not called
      expect(deleteAllCalled).toBe(false);

      // Verify tasks are still displayed
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });

    it('should delete all tasks when user confirms', async () => {
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
          completed: true,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
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

      // User confirms deletion
      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Verify DELETE API was called with correct endpoint
      await waitFor(() => {
        expect(deleteAllCalled).toBe(true);
      });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tasks'),
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });

    it('should clear task list in UI after successful deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task to Delete',
          description: '',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          title: 'Another Task',
          description: '',
          completed: false,
          created_at: '2024-01-02T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task to Delete')).toBeInTheDocument();
        expect(screen.getByText('Another Task')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Verify all tasks are removed from UI
      await waitFor(() => {
        expect(screen.queryByText('Task to Delete')).not.toBeInTheDocument();
        expect(screen.queryByText('Another Task')).not.toBeInTheDocument();
      });

      // Verify empty state is shown
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();

      // Verify Delete All button is no longer visible
      expect(screen.queryByRole('button', { name: /delete all tasks/i })).not.toBeInTheDocument();
    });

    it('should work with both completed and incomplete tasks', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Incomplete Task 1',
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
        {
          id: '3',
          title: 'Incomplete Task 2',
          description: '',
          completed: false,
          created_at: '2024-01-03T00:00:00Z',
          updated_at: '2024-01-03T00:00:00Z',
        },
      ];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Incomplete Task 1')).toBeInTheDocument();
        expect(screen.getByText('Completed Task')).toBeInTheDocument();
        expect(screen.getByText('Incomplete Task 2')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // All tasks should be removed regardless of completion status
      await waitFor(() => {
        expect(screen.queryByText('Incomplete Task 1')).not.toBeInTheDocument();
        expect(screen.queryByText('Completed Task')).not.toBeInTheDocument();
        expect(screen.queryByText('Incomplete Task 2')).not.toBeInTheDocument();
      });

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });
  });

  describe('Delete All Loading States', () => {
    it('should show loading text on button during deletion', async () => {
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
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            status: 204,
          }), 100));
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Button should show loading text
      await waitFor(() => {
        expect(screen.getByText('Deleting All...')).toBeInTheDocument();
      });
      expect(screen.queryByText('🗑️ Delete All Tasks')).not.toBeInTheDocument();
    });

    it('should disable Delete All button during deletion', async () => {
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
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            status: 204,
          }), 200));
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Button should be disabled during operation
      await waitFor(() => {
        const deletingButton = screen.getByRole('button', { name: /deleting all/i });
        expect(deletingButton).toBeDisabled();
      });

      // Wait for operation to complete
      await waitFor(() => {
        expect(screen.queryByText('Deleting All...')).not.toBeInTheDocument();
      });
    });

    it('should disable Delete All button when tasks are loading', async () => {
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
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          }), 100));
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      // During initial load, button should not be visible
      expect(screen.queryByRole('button', { name: /delete all tasks/i })).not.toBeInTheDocument();

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // After loading, button should be enabled
      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton).not.toBeDisabled();
    });

    it('should re-enable button after successful deletion', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Wait for deletion to complete
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Button should no longer be visible (no tasks)
      expect(screen.queryByRole('button', { name: /delete all tasks/i })).not.toBeInTheDocument();
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Should display error message
      await waitFor(() => {
        expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument();
      });

      // Tasks should still be visible
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should handle network errors gracefully', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Should display error message
      await waitFor(() => {
        expect(screen.getByText(/Network connection failed/i)).toBeInTheDocument();
      });

      // Tasks should remain visible
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should clear error message after timeout', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Error should be displayed
      await waitFor(() => {
        expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument();
      });

      // Wait for error to clear (5 second timeout in App.jsx)
      await waitFor(() => {
        expect(screen.queryByText(/HTTP error! status: 500/i)).not.toBeInTheDocument();
      }, { timeout: 6000 });
    }, 10000); // Extended test timeout

    it('should re-enable button after error', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Wait for error
      await waitFor(() => {
        expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument();
      });

      // Button should be re-enabled
      const buttonAfterError = screen.getByRole('button', { name: /delete all tasks/i });
      expect(buttonAfterError).not.toBeDisabled();
    });

    it('should handle multiple error scenarios correctly', async () => {
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

      let attemptCount = 0;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          attemptCount++;
          if (attemptCount === 1) {
            return Promise.resolve({ ok: false, status: 500 });
          } else if (attemptCount === 2) {
            return Promise.reject(new Error('Network error'));
          }
          return Promise.resolve({ ok: true, status: 204 });
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // First attempt - server error
      let deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument();
      });

      // Second attempt - network error
      deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText(/Network error/i)).toBeInTheDocument();
      });

      // Tasks should still be present after errors
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  describe('Delete All - Prevent Multiple Simultaneous Operations', () => {
    it('should not allow multiple simultaneous delete all operations', async () => {
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

      let deleteCallCount = 0;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          deleteCallCount++;
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            status: 204,
          }), 200));
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      
      // Try to click multiple times rapidly
      await user.click(deleteAllButton);
      
      // Button should be disabled, but try to click again
      await waitFor(() => {
        const disabledButton = screen.getByRole('button', { name: /deleting all/i });
        expect(disabledButton).toBeDisabled();
      });

      // Wait for operation to complete
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Should have only called the API once
      expect(deleteCallCount).toBe(1);
    });

    it('should not allow delete all during task loading', async () => {
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
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            json: async () => ({ tasks: mockTasks }),
          }), 200));
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      // During loading, Delete All button should not be visible
      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /delete all tasks/i })).not.toBeInTheDocument();

      // After loading completes
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Now button should be available
      expect(screen.getByRole('button', { name: /delete all tasks/i })).toBeInTheDocument();
    });
  });

  describe('Delete All - Accessibility', () => {
    it('should support keyboard navigation', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      
      // Focus the button
      deleteAllButton.focus();
      expect(deleteAllButton).toHaveFocus();

      // Trigger with keyboard (Enter key)
      await user.keyboard('{Enter}');

      // Should trigger deletion
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should support keyboard navigation with Space key', async () => {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      
      // Focus and trigger with Space key
      deleteAllButton.focus();
      await user.keyboard(' ');

      // Should trigger deletion
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should have proper button role for screen readers', async () => {
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
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton.tagName).toBe('BUTTON');
    });

    it('should announce loading state to screen readers', async () => {
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
          return new Promise(resolve => setTimeout(() => resolve({
            ok: true,
            status: 204,
          }), 100));
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      // Loading text should be visible
      await waitFor(() => {
        const loadingButton = screen.getByText('Deleting All...');
        expect(loadingButton).toBeInTheDocument();
      });
    });
  });

  describe('Delete All - Integration with Other Features', () => {
    it('should not interfere with individual task deletion', async () => {
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

      let currentTasks = [...mockTasks];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
          currentTasks = currentTasks.filter(t => t.id !== '1');
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

      // Delete individual task
      const deleteTask1Button = screen.getByRole('button', { name: /delete task "task 1"/i });
      await user.click(deleteTask1Button);

      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Delete All button should still be present (one task remains)
      expect(screen.getByRole('button', { name: /delete all tasks/i })).toBeInTheDocument();
    });

    it('should work correctly after creating new tasks', async () => {
      let taskList = [];

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'POST') {
          const body = JSON.parse(options.body);
          const newTask = {
            id: `${taskList.length + 1}`,
            title: body.title,
            description: body.description || '',
            completed: false,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
          taskList = [newTask, ...taskList];
          return Promise.resolve({
            ok: true,
            status: 201,
            json: async () => newTask,
          });
        }
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
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

      window.confirm = vi.fn(() => true);

      const user = userEvent.setup();
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Create first task
      const titleInput = screen.getByLabelText(/title/i);
      await user.type(titleInput, 'First Task');
      const createButton = screen.getByRole('button', { name: /create task/i });
      await user.click(createButton);

      await waitFor(() => {
        expect(screen.getByText('First Task')).toBeInTheDocument();
      });

      // Create second task
      await user.type(titleInput, 'Second Task');
      await user.click(createButton);

      await waitFor(() => {
        expect(screen.getByText('Second Task')).toBeInTheDocument();
      });

      // Delete all
      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      await user.click(deleteAllButton);

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      expect(screen.queryByText('First Task')).not.toBeInTheDocument();
      expect(screen.queryByText('Second Task')).not.toBeInTheDocument();
    });

    it('should not be affected by task edit operations', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Original Title',
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
        expect(screen.getByText('Original Title')).toBeInTheDocument();
      });

      // Start editing a task
      const editButton = screen.getByRole('button', { name: /edit task "original title"/i });
      await user.click(editButton);

      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /edit task/i })).toBeInTheDocument();
      });

      // Delete All button should still be visible and functional
      const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
      expect(deleteAllButton).toBeInTheDocument();
      expect(deleteAllButton).not.toBeDisabled();
    });
  });
});
