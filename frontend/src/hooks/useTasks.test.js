/**
 * Property-based tests for useTasks hook
 * Tests universal properties that should hold across all hook operations
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import * as fc from 'fast-check';
import { useTasks } from './useTasks';
import { taskApi } from '../services/api';

// Mock the taskApi module
vi.mock('../services/api', () => ({
  taskApi: {
    getAllTasks: vi.fn(),
    createTask: vi.fn(),
    updateTask: vi.fn(),
    deleteTask: vi.fn(),
    deleteAllTasks: vi.fn(),
    getTaskById: vi.fn(),
  },
}));

describe('useTasks Hook Property Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // Simple sanity test first
  it('sanity check: hook can be rendered and completes initial fetch', async () => {
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });
    
    const { result } = renderHook(() => useTasks());
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });
    
    expect(result.current.tasks).toEqual([]);
  });

  /**
   * Property 2: Hook state management
   * Feature: api-and-frontend-restructure, Property 2: Hook state management
   * Validates: Requirements 9.2
   * 
   * For any task operation performed through the useTasks hook, 
   * the hook should properly manage loading state (true during operation, false after completion)
   * 
   * Note: The loading state in useTasks is specifically for fetchTasks operations.
   * This simplified version tests explicit fetchTasks calls after mount to avoid timing issues.
   */
  it('Property 2: Hook loading state is false after explicit fetchTasks completes', async () => {
    // Generator for ISO date strings
    const isoDateArb = fc.integer({ min: 1577836800000, max: 1767225600000 }).map(ts => new Date(ts).toISOString());
    
    // Generator for task objects
    const taskArb = fc.record({
      id: fc.uuid(),
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.string({ maxLength: 500 }),
      completed: fc.boolean(),
      created_at: isoDateArb,
      updated_at: isoDateArb,
    });

    // Set up initial mock for mount
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    // Render the hook once before the property test
    const { result } = renderHook(() => useTasks());

    // Wait for initial mount fetch to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });

    // Now run property test on explicit fetchTasks calls
    await fc.assert(
      fc.asyncProperty(
        fc.array(taskArb, { minLength: 0, maxLength: 10 }),
        async (tasks) => {
          // Update mock for this iteration
          taskApi.getAllTasks.mockResolvedValue({ tasks });

          // Call fetchTasks explicitly
          await act(async () => {
            await result.current.fetchTasks();
          });

          // Property: Loading should be false after fetchTasks completes
          expect(result.current.loading).toBe(false);
          
          // Property: Tasks should be updated with the fetched data
          expect(result.current.tasks).toEqual(tasks);
        }
      ),
      { numRuns: 100 } // Run 100 iterations as specified in design doc
    );
  });

  /**
   * Property 3: Hook state updates after operations
   * Feature: api-and-frontend-restructure, Property 3: Hook state updates after operations
   * Validates: Requirements 9.4
   * 
   * For any successful task operation (create, update, delete), 
   * the tasks state in the hook should reflect the change immediately after the operation completes
   */
  it('Property 3: Hook state reflects changes after successful operations', async () => {
    // Generator for ISO date strings
    const isoDateArb = fc.integer({ min: 1577836800000, max: 1767225600000 }).map(ts => new Date(ts).toISOString());
    
    // Generator for task objects
    const taskArb = fc.record({
      id: fc.uuid(),
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.string({ maxLength: 500 }),
      completed: fc.boolean(),
      created_at: isoDateArb,
      updated_at: isoDateArb,
    });

    // Generator for task creation data
    const taskCreateArb = fc.record({
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
    });

    // Generator for task update data
    const taskUpdateArb = fc.record({
      title: fc.option(fc.string({ minLength: 1, maxLength: 100 }), { nil: undefined }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
      completed: fc.option(fc.boolean(), { nil: undefined }),
    });

    // Set up initial mock for mount
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    // Render the hook once before the property test
    const { result } = renderHook(() => useTasks());

    // Wait for initial mount fetch to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });

    // Test create operation
    await fc.assert(
      fc.asyncProperty(
        taskCreateArb,
        taskArb,
        async (createData, newTask) => {
          // Mock createTask to return the new task
          taskApi.createTask.mockResolvedValue(newTask);

          const initialLength = result.current.tasks.length;

          // Create a task
          await act(async () => {
            await result.current.createTask(createData);
          });

          // Property: Tasks array should grow by 1
          expect(result.current.tasks.length).toBe(initialLength + 1);
          
          // Property: New task should be at the beginning of the array
          expect(result.current.tasks[0]).toEqual(newTask);
        }
      ),
      { numRuns: 50 } // Run 50 iterations for create
    );

    // Test update operation
    await fc.assert(
      fc.asyncProperty(
        taskArb,
        taskUpdateArb,
        async (existingTask, updateData) => {
          // Add the existing task to the state first
          taskApi.createTask.mockResolvedValue(existingTask);
          await act(async () => {
            await result.current.createTask({ title: existingTask.title, description: existingTask.description });
          });

          // Create updated task
          const updatedTask = { ...existingTask, ...updateData };
          taskApi.updateTask.mockResolvedValue(updatedTask);

          // Update the task
          await act(async () => {
            await result.current.updateTask(existingTask.id, updateData);
          });

          // Property: Task should be updated in the array
          const foundTask = result.current.tasks.find(t => t.id === existingTask.id);
          expect(foundTask).toEqual(updatedTask);
        }
      ),
      { numRuns: 50 } // Run 50 iterations for update
    );

    // Test delete operation
    await fc.assert(
      fc.asyncProperty(
        taskArb,
        async (taskToDelete) => {
          // Add the task to the state first
          taskApi.createTask.mockResolvedValue(taskToDelete);
          await act(async () => {
            await result.current.createTask({ title: taskToDelete.title, description: taskToDelete.description });
          });

          const lengthBeforeDelete = result.current.tasks.length;

          // Mock deleteTask
          taskApi.deleteTask.mockResolvedValue();

          // Delete the task
          await act(async () => {
            await result.current.deleteTask(taskToDelete.id);
          });

          // Property: Tasks array should shrink by 1
          expect(result.current.tasks.length).toBe(lengthBeforeDelete - 1);
          
          // Property: Deleted task should not be in the array
          const foundTask = result.current.tasks.find(t => t.id === taskToDelete.id);
          expect(foundTask).toBeUndefined();
        }
      ),
      { numRuns: 50 } // Run 50 iterations for delete
    );
  });

  /**
   * Property 3b: Hook state clears after deleteAllTasks
   * Tests that deleteAllTasks removes all tasks from state
   */
  it('Property 3b: Hook state clears after successful deleteAllTasks', async () => {
    // Generator for ISO date strings
    const isoDateArb = fc.integer({ min: 1577836800000, max: 1767225600000 }).map(ts => new Date(ts).toISOString());
    
    // Generator for task objects
    const taskArb = fc.record({
      id: fc.uuid(),
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.string({ maxLength: 500 }),
      completed: fc.boolean(),
      created_at: isoDateArb,
      updated_at: isoDateArb,
    });

    // Set up initial mock for mount
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    // Render the hook once before the property test
    const { result } = renderHook(() => useTasks());

    // Wait for initial mount fetch to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });

    await fc.assert(
      fc.asyncProperty(
        fc.array(taskArb, { minLength: 1, maxLength: 10 }),
        async (tasks) => {
          // Add multiple tasks to the state
          for (const task of tasks) {
            taskApi.createTask.mockResolvedValue(task);
            await act(async () => {
              await result.current.createTask({ title: task.title, description: task.description });
            });
          }

          // Verify tasks were added
          expect(result.current.tasks.length).toBeGreaterThan(0);

          // Mock deleteAllTasks
          taskApi.deleteAllTasks.mockResolvedValue();

          // Delete all tasks
          await act(async () => {
            await result.current.deleteAllTasks();
          });

          // Property: Tasks array should be empty
          expect(result.current.tasks).toEqual([]);
          expect(result.current.tasks.length).toBe(0);
        }
      ),
      { numRuns: 50 } // Run 50 iterations for deleteAllTasks
    );
  });

  /**
   * Property 4: Hook error propagation
   * Feature: api-and-frontend-restructure, Property 4: Hook error propagation
   * Validates: Requirements 9.5
   * 
   * For any failed task operation, the useTasks hook should capture the error 
   * and expose it through the error state
   */
  it('Property 4: Hook captures and exposes errors from failed operations', async () => {
    // Generator for error messages
    const errorMessageArb = fc.string({ minLength: 1, maxLength: 200 });

    // Generator for task creation data
    const taskCreateArb = fc.record({
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
    });

    // Generator for task IDs
    const taskIdArb = fc.uuid();

    // Generator for task update data
    const taskUpdateArb = fc.record({
      title: fc.option(fc.string({ minLength: 1, maxLength: 100 }), { nil: undefined }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
      completed: fc.option(fc.boolean(), { nil: undefined }),
    });

    // Set up initial mock for mount
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    // Render the hook once before the property test
    const { result } = renderHook(() => useTasks());

    // Wait for initial mount fetch to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });

    // Test error propagation for fetchTasks
    await fc.assert(
      fc.asyncProperty(
        errorMessageArb,
        async (errorMessage) => {
          // Mock fetchTasks to throw an error
          taskApi.getAllTasks.mockRejectedValue(new Error(errorMessage));

          // Call fetchTasks
          await act(async () => {
            await result.current.fetchTasks();
          });

          // Property: Error should be captured and exposed
          expect(result.current.error).toBe(errorMessage);
        }
      ),
      { numRuns: 30 } // Run 30 iterations for fetchTasks errors
    );

    // Test error propagation for createTask
    await fc.assert(
      fc.asyncProperty(
        taskCreateArb,
        errorMessageArb,
        async (createData, errorMessage) => {
          // Mock createTask to throw an error
          taskApi.createTask.mockRejectedValue(new Error(errorMessage));

          // Call createTask
          await act(async () => {
            await result.current.createTask(createData);
          });

          // Property: Error should be captured and exposed
          expect(result.current.error).toBe(errorMessage);
        }
      ),
      { numRuns: 30 } // Run 30 iterations for createTask errors
    );

    // Test error propagation for updateTask
    await fc.assert(
      fc.asyncProperty(
        taskIdArb,
        taskUpdateArb,
        errorMessageArb,
        async (taskId, updateData, errorMessage) => {
          // Mock updateTask to throw an error
          taskApi.updateTask.mockRejectedValue(new Error(errorMessage));

          // Call updateTask
          await act(async () => {
            await result.current.updateTask(taskId, updateData);
          });

          // Property: Error should be captured and exposed
          expect(result.current.error).toBe(errorMessage);
        }
      ),
      { numRuns: 30 } // Run 30 iterations for updateTask errors
    );

    // Test error propagation for deleteTask
    await fc.assert(
      fc.asyncProperty(
        taskIdArb,
        errorMessageArb,
        async (taskId, errorMessage) => {
          // Mock deleteTask to throw an error (non-404)
          taskApi.deleteTask.mockRejectedValue(new Error(errorMessage));

          // Call deleteTask
          await act(async () => {
            await result.current.deleteTask(taskId);
          });

          // Property: Error should be captured and exposed
          expect(result.current.error).toBe(errorMessage);
        }
      ),
      { numRuns: 30 } // Run 30 iterations for deleteTask errors
    );

    // Test error propagation for deleteAllTasks
    await fc.assert(
      fc.asyncProperty(
        errorMessageArb,
        async (errorMessage) => {
          // Mock deleteAllTasks to throw an error
          taskApi.deleteAllTasks.mockRejectedValue(new Error(errorMessage));

          // Call deleteAllTasks
          await act(async () => {
            await result.current.deleteAllTasks();
          });

          // Property: Error should be captured and exposed
          expect(result.current.error).toBe(errorMessage);
        }
      ),
      { numRuns: 30 } // Run 30 iterations for deleteAllTasks errors
    );
  });

  /**
   * Unit Test: deleteAllTasks rollback on error
   * Tests that deleteAllTasks rolls back state when API call fails
   */
  it('Unit Test: deleteAllTasks rolls back state on error', async () => {
    // Generator for task objects
    const isoDateArb = fc.integer({ min: 1577836800000, max: 1767225600000 }).map(ts => new Date(ts).toISOString());
    const taskArb = fc.record({
      id: fc.uuid(),
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.string({ maxLength: 500 }),
      completed: fc.boolean(),
      created_at: isoDateArb,
      updated_at: isoDateArb,
    });

    // Set up initial mock for mount
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    // Render the hook
    const { result } = renderHook(() => useTasks());

    // Wait for initial mount fetch to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    }, { timeout: 1000 });

    await fc.assert(
      fc.asyncProperty(
        fc.array(taskArb, { minLength: 1, maxLength: 5 }),
        async (tasks) => {
          // Add tasks to the state
          for (const task of tasks) {
            taskApi.createTask.mockResolvedValue(task);
            await act(async () => {
              await result.current.createTask({ title: task.title, description: task.description });
            });
          }

          const originalTasks = [...result.current.tasks];

          // Mock deleteAllTasks to fail
          taskApi.deleteAllTasks.mockRejectedValue(new Error('Delete all failed'));

          // Try to delete all tasks
          await act(async () => {
            await result.current.deleteAllTasks();
          });

          // Property: Tasks should be rolled back to original state
          expect(result.current.tasks).toEqual(originalTasks);
          expect(result.current.tasks.length).toBe(originalTasks.length);
          expect(result.current.error).toBe('Delete all failed');
        }
      ),
      { numRuns: 30 }
    );
  });
});
