import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, screen, waitFor, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { act } from 'react';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

// Helper to flush all pending promises
const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

describe('Delete All Tasks Functionality', () => {
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

  afterEach(async () => {
    // Clean up after each test to prevent state leakage and act() warnings
    await act(async () => {
      cleanup();
      // Allow any pending state updates to complete
      await flushPromises();
    });
  });

  describe('Delete All Button Visibility', () => {
    it('should NOT show Delete All button when there are no tasks', async () => {
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

      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      });

      // Delete All button should not be present
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should show Delete All button when there is at least one task', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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

      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Delete All button should be present
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });

    it('should show Delete All button when there are multiple tasks', async () => {
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
        {
          id: '3',
          title: 'Task 3',
          description: 'Description 3',
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

      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
        expect(screen.getByText('Task 3')).toBeInTheDocument();
      });

      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();
    });
  });

  describe('Delete All Confirmation UI', () => {
    it('should show confirmation message when Delete All is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Confirmation message should appear
      await waitFor(() => {
        expect(
          screen.getByText(
            /are you sure you want to delete all tasks\? this action cannot be undone\./i
          )
        ).toBeInTheDocument();
      });
    });

    it('should show Confirm and Cancel buttons in confirmation state', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Both Confirm and Cancel buttons should appear
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
        expect(
          screen.getByRole('button', { name: /cancel/i })
        ).toBeInTheDocument();
      });

      // Original Delete All button should not be visible
      expect(
        screen.queryByRole('button', { name: /^delete all tasks$/i })
      ).not.toBeInTheDocument();
    });

    it('should hide confirmation UI when Cancel is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Wait for confirmation UI
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      // Click Cancel
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await act(async () => {
        await user.click(cancelButton);
      });

      // Confirmation UI should be hidden
      await waitFor(() => {
        expect(
          screen.queryByText(/are you sure you want to delete all tasks/i)
        ).not.toBeInTheDocument();
        expect(
          screen.queryByRole('button', { name: /confirm delete all/i })
        ).not.toBeInTheDocument();
      });

      // Original Delete All button should be back
      expect(
        screen.getByRole('button', { name: /delete all tasks/i })
      ).toBeInTheDocument();

      // Tasks should still be present
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });
  });

  describe('Delete All API Integration', () => {
    it('should call DELETE /api/tasks when Confirm Delete All is clicked', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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

      const user = userEvent.setup();
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Click Confirm
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /confirm delete all/i,
      });
      await act(async () => {
        await user.click(confirmButton);
      });

      // Verify DELETE request was made
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/tasks'),
          expect.objectContaining({
            method: 'DELETE',
          })
        );
      });
    });

    it('should clear all tasks from UI after successful deletion', async () => {
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

      let tasksExist = true;

      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/api/tasks') && options?.method === 'DELETE') {
          tasksExist = false;
          return Promise.resolve({
            ok: true,
            status: 204,
          });
        }
        if (url.includes('/api/tasks')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ tasks: tasksExist ? mockTasks : [] }),
          });
        }
        return Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Default' }),
        });
      });

      const user = userEvent.setup();
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /confirm delete all/i,
      });
      await act(async () => {
        await user.click(confirmButton);
      });

      // All tasks should be removed
      await waitFor(
        () => {
          expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
          expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
          expect(screen.getByText('No tasks yet')).toBeInTheDocument();
        },
        { timeout: 3000 }
      );

      // Delete All button should also be hidden
      expect(
        screen.queryByRole('button', { name: /delete all tasks/i })
      ).not.toBeInTheDocument();
    });

    it('should show loading state during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /confirm delete all/i,
      });
      await act(async () => {
        await user.click(confirmButton);
      });

      // Button text should change to "Deleting..."
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /deleting\.\.\./i })
        ).toBeInTheDocument();
      });
    });

    it('should disable buttons during deletion', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /confirm delete all/i,
      });
      await act(async () => {
        await user.click(confirmButton);
      });

      // Buttons should be disabled
      await waitFor(() => {
        const deletingButton = screen.getByRole('button', {
          name: /deleting\.\.\./i,
        });
        expect(deletingButton).toBeDisabled();

        const cancelButton = screen.getByRole('button', { name: /cancel/i });
        expect(cancelButton).toBeDisabled();
      });
    });

    it('should handle API errors gracefully', async () => {
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Task 1')).toBeInTheDocument();
      });

      // Click Delete All and confirm
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      const confirmButton = screen.getByRole('button', {
        name: /confirm delete all/i,
      });
      await act(async () => {
        await user.click(confirmButton);
      });

      // Wait for error message to appear
      await waitFor(
        () => {
          const taskListSection = document.querySelector('.task-list-section');
          expect(taskListSection.textContent).toMatch(
            /HTTP error! status: 500/i
          );
        },
        { timeout: 3000 }
      );

      // Wait for confirmation UI to be dismissed (Delete All button reappears)
      await waitFor(
        () => {
          expect(
            screen.getByRole('button', { name: /delete all tasks/i })
          ).toBeInTheDocument();
        },
        { timeout: 3000 }
      );

      // Tasks should still be present (no removal on error)
      await waitFor(
        () => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        },
        { timeout: 3000 }
      );
    });
  });

  describe('CSS Styling', () => {
    it('should apply correct CSS classes to delete all section', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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

      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Check for delete-all-section class
      const deleteAllSection = document.querySelector('.delete-all-section');
      expect(deleteAllSection).toBeInTheDocument();
      expect(deleteAllSection).not.toHaveClass('confirming');
    });

    it('should apply confirming class when in confirmation state', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      // Click Delete All button
      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Check for confirming class
      await waitFor(() => {
        const deleteAllSection = document.querySelector('.delete-all-section');
        expect(deleteAllSection).toHaveClass('confirming');
      });
    });
  });

  describe('Edge Cases', () => {
    it('should handle rapid clicks on Delete All button', async () => {
      const mockTasks = [
        {
          id: '1',
          title: 'Test Task',
          description: 'Test Description',
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
      await act(async () => {
        render(<App />);
      });

      await waitFor(() => {
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });

      const deleteAllButton = screen.getByRole('button', {
        name: /delete all tasks/i,
      });

      // Click the button once to enter confirmation state
      await act(async () => {
        await user.click(deleteAllButton);
      });

      // Wait for confirmation UI to appear
      await waitFor(() => {
        expect(
          screen.getByRole('button', { name: /confirm delete all/i })
        ).toBeInTheDocument();
      });

      // Try to click again (button should no longer be available)
      const deleteAllButtonAfterClick = screen.queryByRole('button', {
        name: /^delete all tasks$/i,
      });
      expect(deleteAllButtonAfterClick).not.toBeInTheDocument();

      // Should only show confirmation once
      const confirmButtons = screen.getAllByRole('button', {
        name: /confirm delete all/i,
      });
      expect(confirmButtons).toHaveLength(1);
    });

    it(
      'should handle network errors during deletion',
      async () => {
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

        // Keep track of calls to ensure consistency
        let deleteCallCount = 0;

        global.fetch.mockImplementation((url, options) => {
          if (url.includes('/api/tasks') && options?.method === 'DELETE') {
            deleteCallCount++;
            return Promise.reject(new Error('Network error'));
          }
          // Always return the same tasks on GET regardless of DELETE failures
          if (url.includes('/api/tasks') && !options?.method) {
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
        await act(async () => {
          render(<App />);
        });

        await waitFor(() => {
          expect(screen.getByText('Task 1')).toBeInTheDocument();
        });

        // Click Delete All and confirm
        const deleteAllButton = screen.getByRole('button', {
          name: /delete all tasks/i,
        });
        await act(async () => {
          await user.click(deleteAllButton);
        });

        await waitFor(() => {
          expect(
            screen.getByRole('button', { name: /confirm delete all/i })
          ).toBeInTheDocument();
        });

        const confirmButton = screen.getByRole('button', {
          name: /confirm delete all/i,
        });

        // Click confirm and wait for all state updates
        await act(async () => {
          await user.click(confirmButton);
          // Give more time for the error to propagate and state updates to complete
          await new Promise((resolve) => setTimeout(resolve, 500));
        });

        // Verify DELETE was attempted
        await waitFor(
          () => {
            expect(deleteCallCount).toBeGreaterThan(0);
          },
          { timeout: 10000 }
        );

        // Wait for error message to appear
        await waitFor(
          () => {
            const taskListSection =
              document.querySelector('.task-list-section');
            expect(taskListSection.textContent).toMatch(/Network error/i);
          },
          { timeout: 10000 }
        );

        // Wait for confirmation UI to be dismissed (Delete All button reappears)
        await waitFor(
          () => {
            expect(
              screen.getByRole('button', { name: /delete all tasks/i })
            ).toBeInTheDocument();
          },
          { timeout: 10000 }
        );

        // FIX: Tasks should REMAIN after network error (useTasks hook preserves tasks on error)
        // The hook does NOT clear tasks on error - it keeps them visible
        await waitFor(
          () => {
            const tasksList = screen.queryAllByRole('listitem');
            expect(tasksList).toHaveLength(1); // Tasks should still be present
            expect(screen.getByText('Task 1')).toBeInTheDocument();
          },
          { timeout: 10000 }
        );
      },
      25000
    ); // Add 25 second timeout to handle all waitFor calls with 10s timeouts
  });
});
