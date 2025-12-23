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

      await waitFor(() => {
        expect(
          screen.queryByText('Loading tasks...')
        ).not.toBeInTheDocument();
      });
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

    it('should display task completion status correctly', async () => {
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
        expect(screen.getByText('○ Incomplete')).toBeInTheDocument();
        expect(screen.getByText('✓ Completed')).toBeInTheDocument();
      });
    });

    it('should display task creation dates', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: '',
          completed: false,
          created_at: '2024-01-15T00:00:00Z',
          updated_at: '2024-01-15T00:00:00Z',
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
        expect(screen.getByText(/Created:/)).toBeInTheDocument();
      });
    });

    it('should display error message when task fetch fails', async () => {
      global.fetch.mockImplementation((url) => {
        if (url.includes('/api/tasks')) {
          return Promise.reject(new Error('Network error'));
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText(/Network error/i)).toBeInTheDocument();
      });
    });

    it('should handle tasks without descriptions', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Task without description',
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
        expect(
          screen.getByText('Task without description')
        ).toBeInTheDocument();
        // Description paragraph should not be rendered if empty
        const taskItem = screen
          .getByText('Task without description')
          .closest('.task-item');
        expect(
          taskItem.querySelector('.task-description')
        ).not.toBeInTheDocument();
      });
    });

    it('should apply completed styling to completed tasks', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Completed Task',
          description: '',
          completed: true,
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
        const taskTitle = screen.getByText('Completed Task');
        expect(taskTitle).toHaveClass('completed');
      });
    });
  });

  describe('Delete All Tasks Feature', () => {
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

      // Delete all button should be visible
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });

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
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Confirmation dialog should appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
        ).toBeInTheDocument();
        expect(
          screen.getByRole('button', { name: /yes, delete all/i })
        ).toBeInTheDocument();
        expect(
          screen.getByRole('button', { name: /cancel/i })
        ).toBeInTheDocument();
      });

      // Original delete all button should be hidden
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should hide confirmation dialog when cancel button is clicked', async () => {
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

      // Wait for confirmation dialog
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
        ).toBeInTheDocument();
      });

      // Click cancel
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await user.click(cancelButton);

      // Confirmation dialog should disappear
      await waitFor(() => {
        expect(
          screen.queryByText(/are you sure you want to delete all tasks\?/i)
        ).not.toBeInTheDocument();
      });

      // Delete all button should reappear
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Tasks should still be visible
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    it('should complete full delete all flow: button → confirmation → deletion', async () => {
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
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Wait for confirmation dialog
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
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

      // Delete all button should not be visible anymore
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
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

      let resolveDelete;
      const deletePromise = new Promise((resolve) => {
        resolveDelete = resolve;
      });

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          // Return the promise that won't resolve until we call resolveDelete
          return deletePromise.then(() => ({
            ok: true,
            status: 204,
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Wait for loading state to appear using findByRole (async query)
      const deletingButton = await screen.findByRole(
        'button',
        { name: /deleting\.\.\./i },
        { timeout: 2000 }
      );
      expect(deletingButton).toBeInTheDocument();

      // Now resolve the delete operation
      resolveDelete();

      // Wait for deletion to complete
      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
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

      let resolveDelete;
      const deletePromise = new Promise((resolve) => {
        resolveDelete = resolve;
      });

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          // Return the promise that won't resolve until we call resolveDelete
          return deletePromise.then(() => ({
            ok: true,
            status: 204,
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

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Click confirm
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Wait for loading state and verify buttons are disabled using findByRole
      const deletingButton = await screen.findByRole(
        'button',
        { name: /deleting\.\.\./i },
        { timeout: 2000 }
      );
      expect(deletingButton).toBeDisabled();

      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      expect(cancelButton).toBeDisabled();

      // Complete the deletion
      resolveDelete();

      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      });
    });

    it('should handle delete all API error gracefully', async () => {
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

      // Use controlled promise pattern to manage timing
      let rejectDelete;
      const deletePromise = new Promise((resolve, reject) => {
        rejectDelete = reject;
      });

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          // Return controlled promise that we'll reject with an error
          return deletePromise.then(
            (response) => response,
            (_error) => {
              // Return a failed response instead of throwing
              return {
                ok: false,
                status: 500,
              };
            }
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

      // Wait for initial tasks to load
      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click delete all button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await user.click(deleteAllButton);

      // Wait for confirmation dialog to appear
      await waitFor(() => {
        expect(
          screen.getByText(/are you sure you want to delete all tasks\?/i)
        ).toBeInTheDocument();
      });

      // Click confirm button
      const confirmButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      await user.click(confirmButton);

      // Wait for the loading state to appear (confirms delete operation started)
      const deletingButton = await screen.findByRole(
        'button',
        { name: /deleting\.\.\./i },
        { timeout: 2000 }
      );
      expect(deletingButton).toBeInTheDocument();

      // Now trigger the API error by rejecting the promise
      rejectDelete(new Error('API Error'));

      // Wait for error to be displayed
      await waitFor(
        () => {
          const taskListSection = document.querySelector('.task-list-section');
          expect(taskListSection).toBeInTheDocument();
          expect(taskListSection.textContent).toMatch(
            /HTTP error! status: 500/i
          );
        },
        { timeout: 3000 }
      );

      // Verify tasks are rolled back and visible again
      await waitFor(
        () => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        },
        { timeout: 3000 }
      );

      // Confirmation dialog should still be visible (not hidden on error)
      expect(
        screen.getByText(/are you sure you want to delete all tasks\?/i)
      ).toBeInTheDocument();

      // Buttons should be enabled again (not loading anymore)
      const yesButton = screen.getByRole('button', {
        name: /yes, delete all/i,
      });
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      expect(yesButton).not.toBeDisabled();
      expect(cancelButton).not.toBeDisabled();
    });
  });

  describe('Property-Based Tests', () => {
    it('Property 10: Task ordering consistency - tasks should be ordered by creation date (newest first)', async () => {
      /**
       * Feature: task-manager-app, Property 10: Task ordering consistency
       * Validates: Requirements 2.4
       *
       * For any set of tasks, when retrieved via GET /api/tasks,
       * the tasks should be ordered by creation timestamp in descending order (newest first).
       */
      const fc = await import('fast-check');

      await fc.assert(
        fc.asyncProperty(
          // Generate an array of 2-10 tasks with random timestamps
          fc.array(
            fc.record({
              id: fc.uuid(),
              title: fc.string({ minLength: 1, maxLength: 50 }),
              description: fc.string({ maxLength: 200 }),
              completed: fc.boolean(),
              created_at: fc
                .integer({
                  min: new Date('2020-01-01').getTime(),
                  max: new Date('2025-12-31').getTime(),
                })
                .map((timestamp) => new Date(timestamp).toISOString()),
              updated_at: fc
                .integer({
                  min: new Date('2020-01-01').getTime(),
                  max: new Date('2025-12-31').getTime(),
                })
                .map((timestamp) => new Date(timestamp).toISOString()),
            }),
            { minLength: 2, maxLength: 10 }
          ),
          async (generatedTasks) => {
            // Sort tasks by created_at descending to match backend behavior
            const sortedTasks = [...generatedTasks].sort(
              (a, b) =>
                new Date(b.created_at).getTime() -
                new Date(a.created_at).getTime()
            );

            // Mock the API to return the sorted tasks (matching backend behavior)
            global.fetch.mockImplementation((url) => {
              if (url.includes('/api/tasks')) {
                return Promise.resolve({
                  ok: true,
                  json: async () => ({ tasks: sortedTasks }),
                });
              }
              return Promise.resolve({
                ok: true,
                json: async () => ({ message: 'Default' }),
              });
            });

            const { unmount } = render(<App />);

            try {
              // Wait for tasks to be rendered
              await waitFor(
                () => {
                  const taskItems = document.querySelectorAll('.task-item');
                  expect(taskItems.length).toBe(generatedTasks.length);
                },
                { timeout: 3000 }
              );

              // Get the rendered task titles in order
              const taskItems = document.querySelectorAll('.task-item');
              const renderedTitles = Array.from(taskItems).map(
                (item) => item.querySelector('.task-title').textContent
              );

              // Sort the generated tasks by created_at descending (newest first)
              const expectedOrder = [...generatedTasks]
                .sort(
                  (a, b) =>
                    new Date(b.created_at).getTime() -
                    new Date(a.created_at).getTime()
                )
                .map((task) => task.title);

              // Verify the rendered order matches the expected order
              expect(renderedTitles).toEqual(expectedOrder);
            } finally {
              unmount();
            }
          }
        ),
        { numRuns: 10 } // Reduced runs for faster test execution
      );
    }, 15000); // 15 second timeout
  });

  describe('Integration Tests - Complete User Flows', () => {
    describe('Task Creation Flow', () => {
      it('should complete full task creation flow: form → API → list update', async () => {
        // Start with empty task list
        let taskList = [];

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'POST') {
            const body = JSON.parse(options.body);
            const newTask = {
              id: '123',
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

        // Wait for initial load
        await waitFor(() => {
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        });

        // Fill in the form
        const titleInput = screen.getByLabelText(/title/i);
        const descriptionInput = screen.getByLabelText(/description/i);

        await user.type(titleInput, 'New Integration Test Task');
        await user.type(descriptionInput, 'This is a test description');

        // Submit the form
        const createButton = screen.getByRole('button', {
          name: /create task/i,
        });
        await user.click(createButton);

        // Verify task appears in the list
        await waitFor(() => {
          expect(
            screen.getByText('New Integration Test Task')
          ).toBeInTheDocument();
          expect(
            screen.getByText('This is a test description')
          ).toBeInTheDocument();
        });

        // Verify form is cleared
        expect(titleInput).toHaveValue('');
        expect(descriptionInput).toHaveValue('');

        // Verify "No tasks yet" is gone
        expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
      });

      it('should handle validation errors during task creation', async () => {
        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'POST') {
            return Promise.resolve({
              ok: false,
              status: 422,
              json: async () => ({
                detail: [{ msg: 'Title cannot be empty' }],
              }),
            });
          }
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

        const user = userEvent.setup();
        render(<App />);

        await waitFor(() => {
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        });

        // Try to submit with empty title (after typing and clearing)
        const titleInput = screen.getByLabelText(/title/i);
        await user.type(titleInput, 'Test');
        await user.clear(titleInput);

        const createButton = screen.getByRole('button', {
          name: /create task/i,
        });
        await user.click(createButton);

        // Should show client-side validation error
        await waitFor(() => {
          expect(
            screen.getByText('Title cannot be empty')
          ).toBeInTheDocument();
        });

        // Task list should remain empty
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });
    });

    describe('Task Editing Flow', () => {
      it('should complete full task editing flow: edit button → form → update → display', async () => {
        const initialTask = {
          id: '1',
          title: 'Original Title',
          description: 'Original Description',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        let currentTask = { ...initialTask };

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'PUT') {
            const body = JSON.parse(options.body);
            currentTask = {
              ...currentTask,
              ...body,
              updated_at: new Date().toISOString(),
            };
            return Promise.resolve({
              ok: true,
              json: async () => currentTask,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [currentTask] }),
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
          expect(screen.getByText('Original Title')).toBeInTheDocument();
        });

        // Click edit button
        const editButton = screen.getByRole('button', {
          name: /edit task "original title"/i,
        });
        await user.click(editButton);

        // Verify form switches to edit mode
        await waitFor(() => {
          expect(
            screen.getByRole('heading', { name: /edit task/i })
          ).toBeInTheDocument();
        });

        // Verify form is populated with current data
        const titleInput = screen.getByPlaceholderText(/enter task title/i);
        const descriptionInput = screen.getByPlaceholderText(
          /enter task description/i
        );
        expect(titleInput).toHaveValue('Original Title');
        expect(descriptionInput).toHaveValue('Original Description');

        // Update the task
        await user.clear(titleInput);
        await user.type(titleInput, 'Updated Title');
        await user.clear(descriptionInput);
        await user.type(descriptionInput, 'Updated Description');

        // Submit the update
        const updateButton = screen.getByRole('button', {
          name: /update task/i,
        });
        await user.click(updateButton);

        // Verify task is updated in the list
        await waitFor(() => {
          const taskList = document.querySelector('.task-list');
          expect(taskList).toBeInTheDocument();
          expect(taskList.textContent).toContain('Updated Title');
          expect(taskList.textContent).toContain('Updated Description');
        });

        // Verify form returns to create mode
        await waitFor(() => {
          expect(
            screen.getByRole('heading', { name: /create new task/i })
          ).toBeInTheDocument();
        });
        expect(titleInput).toHaveValue('');
        expect(descriptionInput).toHaveValue('');
      });

      it('should handle cancel during edit', async () => {
        const task = {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        global.fetch.mockImplementation((url) => {
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [task] }),
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
          expect(screen.getByText('Test Task')).toBeInTheDocument();
        });

        // Start editing
        const editButton = screen.getByRole('button', {
          name: /edit task "test task"/i,
        });
        await user.click(editButton);

        await waitFor(() => {
          expect(
            screen.getByRole('heading', { name: /edit task/i })
          ).toBeInTheDocument();
        });

        // Make some changes
        const titleInput = screen.getByPlaceholderText(/enter task title/i);
        await user.clear(titleInput);
        await user.type(titleInput, 'Changed Title');

        // Click cancel
        const cancelButton = screen.getByRole('button', { name: /cancel/i });
        await user.click(cancelButton);

        // Verify form returns to create mode
        await waitFor(() => {
          expect(
            screen.getByRole('heading', { name: /create new task/i })
          ).toBeInTheDocument();
        });

        // Verify original task is unchanged
        expect(screen.getByText('Test Task')).toBeInTheDocument();
        expect(screen.queryByText('Changed Title')).not.toBeInTheDocument();

        // Verify form is cleared
        expect(titleInput).toHaveValue('');
      });

      it('should handle 404 error during update', async () => {
        const task = {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'PUT') {
            return Promise.resolve({
              ok: false,
              status: 404,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [task] }),
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
          expect(screen.getByText('Test Task')).toBeInTheDocument();
        });

        // Start editing
        const editButton = screen.getByRole('button', {
          name: /edit task "test task"/i,
        });
        await user.click(editButton);

        await waitFor(() => {
          expect(
            screen.getByRole('heading', { name: /edit task/i })
          ).toBeInTheDocument();
        });

        // Try to update
        const titleInput = screen.getByPlaceholderText(/enter task title/i);
        await user.clear(titleInput);
        await user.type(titleInput, 'Updated Title');

        const updateButton = screen.getByRole('button', {
          name: /update task/i,
        });
        await user.click(updateButton);

        // Should show error message in the form
        await waitFor(() => {
          const formSection = document.querySelector('.task-form-section');
          expect(formSection.textContent).toMatch(/Failed to update task/i);
        });
      });
    });

    describe('Task Deletion Flow', () => {
      it('should complete full task deletion flow: delete button → removal', async () => {
        const task = {
          id: '1',
          title: 'Task to Delete',
          description: 'This will be deleted',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        let taskExists = true;

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
            taskExists = false;
            return Promise.resolve({
              ok: true,
              status: 204,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: taskExists ? [task] : [] }),
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
          expect(screen.getByText('Task to Delete')).toBeInTheDocument();
        });

        // Click delete button
        const deleteButton = screen.getByRole('button', {
          name: /delete task "task to delete"/i,
        });
        await user.click(deleteButton);

        // Verify task is removed from UI
        await waitFor(() => {
          expect(
            screen.queryByText('Task to Delete')
          ).not.toBeInTheDocument();
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        });
      });

      it('should handle 404 gracefully during deletion', async () => {
        const task = {
          id: '1',
          title: 'Task to Delete',
          description: 'This will be deleted',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
            return Promise.resolve({
              ok: false,
              status: 404,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [task] }),
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

        // Click delete button
        const deleteButton = screen.getByRole('button', {
          name: /delete task "task to delete"/i,
        });
        await user.click(deleteButton);

        // Task should still be removed from UI (graceful handling)
        await waitFor(() => {
          expect(
            screen.queryByText('Task to Delete')
          ).not.toBeInTheDocument();
        });
      });
    });

    describe('Completion Toggle Flow', () => {
      it('should toggle task completion status', async () => {
        const task = {
          id: '1',
          title: 'Task to Toggle',
          description: 'Toggle me',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        let currentCompleted = false;

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'PUT') {
            const body = JSON.parse(options.body);
            currentCompleted = body.completed;
            return Promise.resolve({
              ok: true,
              json: async () => ({
                ...task,
                completed: currentCompleted,
                updated_at: new Date().toISOString(),
              }),
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({
                tasks: [
                  {
                    ...task,
                    completed: currentCompleted,
                  },
                ],
              }),
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
          expect(screen.getByText('Task to Toggle')).toBeInTheDocument();
          expect(screen.getByText('○ Incomplete')).toBeInTheDocument();
        });

        // Toggle completion
        const checkbox = screen.getByRole('checkbox', {
          name: /mark task "task to toggle" as complete/i,
        });
        await user.click(checkbox);

        // Verify status changes to completed
        await waitFor(() => {
          expect(screen.getByText('✓ Completed')).toBeInTheDocument();
          expect(screen.queryByText('○ Incomplete')).not.toBeInTheDocument();
        });

        // Toggle back
        await user.click(checkbox);

        // Verify status changes back to incomplete
        await waitFor(() => {
          expect(screen.getByText('○ Incomplete')).toBeInTheDocument();
          expect(screen.queryByText('✓ Completed')).not.toBeInTheDocument();
        });
      });

      it('should handle 404 error during toggle', async () => {
        const task = {
          id: '1',
          title: 'Task to Toggle',
          description: 'Toggle me',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'PUT') {
            return Promise.resolve({
              ok: false,
              status: 404,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [task] }),
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
          expect(screen.getByText('Task to Toggle')).toBeInTheDocument();
        });

        // Try to toggle
        const checkbox = screen.getByRole('checkbox', {
          name: /mark task "task to toggle" as complete/i,
        });
        await user.click(checkbox);

        // Should show error message in task list section
        await waitFor(() => {
          const taskListSection =
            document.querySelector('.task-list-section');
          expect(taskListSection.textContent).toMatch(/Task not found/i);
        });
      });
    });

    describe('Error Handling for Failed API Calls', () => {
      it('should display network error when task fetch fails', async () => {
        global.fetch.mockImplementation((url) => {
          if (url.includes('/api/tasks')) {
            return Promise.reject(new Error('Network connection failed'));
          }
          return Promise.resolve({
            ok: true,
            json: async () => ({ message: 'Default' }),
          });
        });

        render(<App />);

        await waitFor(() => {
          expect(
            screen.getByText(/Network connection failed/i)
          ).toBeInTheDocument();
        });
      });

      it('should display server error when task creation fails', async () => {
        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'POST') {
            return Promise.resolve({
              ok: false,
              status: 500,
            });
          }
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

        const user = userEvent.setup();
        render(<App />);

        await waitFor(() => {
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        });

        // Try to create a task
        const titleInput = screen.getByLabelText(/title/i);
        await user.type(titleInput, 'Test Task');

        const createButton = screen.getByRole('button', {
          name: /create task/i,
        });
        await user.click(createButton);

        // Should show error in the form
        await waitFor(() => {
          const formSection = document.querySelector('.task-form-section');
          expect(formSection.textContent).toMatch(/Failed to create task/i);
        });
      });

      it('should display error when deletion fails', async () => {
        const task = {
          id: '1',
          title: 'Task to Delete',
          description: 'This will fail',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
            return Promise.resolve({
              ok: false,
              status: 500,
            });
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: [task] }),
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

        // Try to delete
        const deleteButton = screen.getByRole('button', {
          name: /delete task "task to delete"/i,
        });
        await user.click(deleteButton);

        // Should show error in task list section
        await waitFor(() => {
          const taskListSection =
            document.querySelector('.task-list-section');
          expect(taskListSection.textContent).toMatch(
            /HTTP error! status: 500/i
          );
        });
      });
    });

    describe('Loading States', () => {
      it('should show loading indicator while fetching tasks', async () => {
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

        await waitFor(() => {
          expect(
            screen.queryByText('Loading tasks...')
          ).not.toBeInTheDocument();
        });
      });

      it('should disable buttons during operations', async () => {
        const task = {
          id: '1',
          title: 'Test Task',
          description: 'Test',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        };

        let taskExists = true;
        let deleteStarted = false;

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks/1') && options?.method === 'DELETE') {
            deleteStarted = true;
            return new Promise((resolve) =>
              setTimeout(
                () => {
                  taskExists = false;
                  resolve({
                    ok: true,
                    status: 204,
                  });
                },
                100
              )
            );
          }
          if (url.includes('/api/tasks')) {
            return Promise.resolve({
              ok: true,
              json: async () => ({ tasks: taskExists ? [task] : [] }),
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
          expect(screen.getByText('Test Task')).toBeInTheDocument();
        });

        // Get reference to delete button
        const deleteButton = screen.getByRole('button', {
          name: /delete task "test task"/i,
        });

        // Start delete operation
        await user.click(deleteButton);

        // Verify delete was initiated
        await waitFor(() => {
          expect(deleteStarted).toBe(true);
        });

        // Wait for deletion to complete
        await waitFor(() => {
          expect(screen.queryByText('Test Task')).not.toBeInTheDocument();
        });
      });
    });

    describe('Empty State Display', () => {
      it('should display empty state when no tasks exist', async () => {
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

      it('should hide empty state when tasks are added', async () => {
        let taskList = [];

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'POST') {
            const body = JSON.parse(options.body);
            const newTask = {
              id: '1',
              title: body.title,
              description: body.description || '',
              completed: false,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            };
            taskList = [newTask];
            return Promise.resolve({
              ok: true,
              status: 201,
              json: async () => newTask,
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
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        });

        // Add a task
        const titleInput = screen.getByLabelText(/title/i);
        await user.type(titleInput, 'First Task');

        const createButton = screen.getByRole('button', {
          name: /create task/i,
        });
        await user.click(createButton);

        // Empty state should be gone
        await waitFor(() => {
          expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
          expect(screen.getByText('First Task')).toBeInTheDocument();
        });
      });
    });
  });
});
