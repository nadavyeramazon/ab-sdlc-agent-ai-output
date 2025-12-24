import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

describe('App Component', () => {
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

  describe('Component Rendering', () => {
    it('should render without crashing', () => {
      render(<App />);
      expect(screen.getByText('Task Manager')).toBeInTheDocument();
    });

    it('should render key UI elements', () => {
      render(<App />);

      // Check for main heading
      expect(
        screen.getByRole('heading', { name: /task manager/i })
      ).toBeInTheDocument();

      // Check for task section
      expect(
        screen.getByRole('heading', { name: /my tasks/i })
      ).toBeInTheDocument();
    });

    it('should have correct initial state', async () => {
      render(<App />);

      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    it('should render with proper CSS classes', () => {
      render(<App />);

      expect(document.querySelector('.app')).toBeInTheDocument();
      expect(document.querySelector('.container')).toBeInTheDocument();
    });
  });

  describe('Delete All Tasks Feature', () => {
    describe('Delete All Button Visibility', () => {
      it('should NOT show delete all button when tasks array is empty', async () => {
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

        // Delete all button should NOT be visible
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

      it('should hide delete all button after all tasks are deleted', async () => {
        let taskList = [
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
          if (url.includes('/api/tasks') && options?.method === 'DELETE' && !url.includes('/api/tasks/')) {
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

        // Wait for task to load
        await waitFor(() => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        });

        // Click delete all button
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirm deletion
        await waitFor(() => {
          expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', { name: /yes, delete all/i });
        await user.click(confirmButton);

        // Wait for deletion to complete
        await waitFor(() => {
          expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        });

        // Delete all button should no longer be visible
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
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirmation dialog should appear
        await waitFor(() => {
          expect(
            screen.getByText(/are you sure you want to delete all tasks/i)
          ).toBeInTheDocument();
        });

        // Should have cancel and confirm buttons
        expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /yes, delete all/i })).toBeInTheDocument();
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

        // Delete all button should be visible
        expect(
          screen.getByRole('button', { name: /delete all tasks/i })
        ).toBeInTheDocument();

        // Click delete all button
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirmation dialog should appear
        await waitFor(() => {
          expect(
            screen.getByText(/are you sure you want to delete all tasks/i)
          ).toBeInTheDocument();
        });

        // Delete all button should no longer be visible
        expect(
          screen.queryByRole('button', { name: /delete all tasks/i })
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
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirmation dialog should appear
        await waitFor(() => {
          expect(
            screen.getByText(/are you sure you want to delete all tasks/i)
          ).toBeInTheDocument();
        });

        // Click cancel
        const cancelButton = screen.getByRole('button', { name: /cancel/i });
        await user.click(cancelButton);

        // Confirmation dialog should disappear
        await waitFor(() => {
          expect(
            screen.queryByText(/are you sure you want to delete all tasks/i)
          ).not.toBeInTheDocument();
        });

        // Task should still be visible
        expect(screen.getByText('Task 1')).toBeInTheDocument();

        // Delete all button should be visible again
        expect(
          screen.getByRole('button', { name: /delete all tasks/i })
        ).toBeInTheDocument();
      });
    });

    describe('Delete All Execution', () => {
      it('should delete all tasks when confirmed', async () => {
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

        let taskList = [...mockTasks];

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'DELETE' && !url.includes('/api/tasks/')) {
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
          expect(screen.getByText('Task 1')).toBeInTheDocument();
          expect(screen.getByText('Task 2')).toBeInTheDocument();
        });

        // Click delete all button
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirm deletion
        await waitFor(() => {
          expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', { name: /yes, delete all/i });
        await user.click(confirmButton);

        // All tasks should be removed
        await waitFor(() => {
          expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
          expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
        });

        // Should show empty state
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();

        // Verify API was called
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/tasks'),
          expect.objectContaining({
            method: 'DELETE',
          })
        );
      });

      it('should show loading state during deletion', async () => {
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
          if (url.includes('/api/tasks') && options?.method === 'DELETE' && !url.includes('/api/tasks/')) {
            return new Promise((resolve) =>
              setTimeout(() =>
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
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirm deletion
        await waitFor(() => {
          expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', { name: /yes, delete all/i });
        await user.click(confirmButton);

        // Should show loading state
        expect(screen.getByText('Deleting...')).toBeInTheDocument();

        // Wait for deletion to complete
        await waitFor(() => {
          expect(screen.queryByText('Deleting...')).not.toBeInTheDocument();
        });
      });

      it('should handle error during delete all operation', async () => {
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
          if (url.includes('/api/tasks') && options?.method === 'DELETE' && !url.includes('/api/tasks/')) {
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

        // Click delete all button
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirm deletion
        await waitFor(() => {
          expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', { name: /yes, delete all/i });
        await user.click(confirmButton);

        // Tasks should still be visible (rollback on error)
        await waitFor(() => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        });

        // Should show error message
        await waitFor(() => {
          const taskListSection = document.querySelector('.task-list-section');
          expect(taskListSection.textContent).toMatch(/HTTP error! status: 500/i);
        });
      });

      it('should disable confirm button during deletion', async () => {
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
          if (url.includes('/api/tasks') && options?.method === 'DELETE' && !url.includes('/api/tasks/')) {
            return new Promise((resolve) =>
              setTimeout(() =>
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
        const deleteAllButton = screen.getByRole('button', { name: /delete all tasks/i });
        await user.click(deleteAllButton);

        // Confirm deletion
        await waitFor(() => {
          expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', { name: /yes, delete all/i });
        await user.click(confirmButton);

        // Confirm button should be disabled during deletion
        await waitFor(() => {
          const confirmBtn = screen.getByRole('button', { name: /deleting/i });
          expect(confirmBtn).toBeDisabled();
        });
      });
    });
  });

  describe('Task List Display', () => {
    it('should fetch tasks on component mount', async () => {
      render(<App />);

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/tasks')
        );
      });
    });

    it('should display "No tasks yet" when task list is empty', async () => {
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
    });

    it('should display loading state while fetching tasks', async () => {
      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  json: async () => ({ tasks: [] }),
                }),
              100
            )
          );
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      expect(screen.getByText('Loading tasks...')).toBeInTheDocument();
    });

    it('should display tasks when API returns task list', async () => {
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
        expect(screen.getByText('Test Task 1')).toBeInTheDocument();
        expect(screen.getByText('Test Task 2')).toBeInTheDocument();
        expect(screen.getByText('Description 1')).toBeInTheDocument();
        expect(screen.getByText('Description 2')).toBeInTheDocument();
      });
    });
  });
});
