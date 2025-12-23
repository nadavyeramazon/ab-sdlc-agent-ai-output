/**
 * Property-based tests for API service
 * Tests universal properties that should hold across all API operations
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as fc from 'fast-check';
import { taskApi } from './api.js';

describe('API Service Property Tests', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  /**
   * Property 1: API error handling consistency
   * Validates: Requirements 7.2, 7.4
   *
   * For any API operation that fails, the error should be caught and
   * formatted consistently with an error message
   */
  it('Property 1: API error handling consistency - all failed operations throw Error with message', async () => {
    // Generator for HTTP error status codes (excluding 404 for delete which is handled specially)
    const httpErrorStatusArb = fc.integer({ min: 400, max: 599 }).filter((status) => status !== 404);

    // Generator for 422 validation errors
    const validationErrorArb = fc.record({
      detail: fc.array(
        fc.record({
          msg: fc.string({ minLength: 1, maxLength: 100 }),
          loc: fc.array(fc.string()),
          type: fc.string(),
        }),
        { minLength: 1, maxLength: 3 }
      ),
    });

    // Generator for task IDs
    const taskIdArb = fc.uuid();

    // Generator for task data
    const taskDataArb = fc.record({
      title: fc.string({ minLength: 1, maxLength: 100 }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
    });

    // Generator for update data
    const updateDataArb = fc.record({
      title: fc.option(fc.string({ minLength: 1, maxLength: 100 }), { nil: undefined }),
      description: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
      completed: fc.option(fc.boolean(), { nil: undefined }),
    });

    await fc.assert(
      fc.asyncProperty(
        fc.oneof(
          // Test getAllTasks with various error statuses
          fc.record({
            method: fc.constant('getAllTasks'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
          }),
          // Test createTask with validation errors
          fc.record({
            method: fc.constant('createTask'),
            status: fc.constant(422),
            hasValidationError: fc.constant(true),
            validationError: validationErrorArb,
            taskData: taskDataArb,
          }),
          // Test createTask with other errors
          fc.record({
            method: fc.constant('createTask'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
            taskData: taskDataArb,
          }),
          // Test updateTask with validation errors
          fc.record({
            method: fc.constant('updateTask'),
            status: fc.constant(422),
            hasValidationError: fc.constant(true),
            validationError: validationErrorArb,
            taskId: taskIdArb,
            updateData: updateDataArb,
          }),
          // Test updateTask with 404 errors
          fc.record({
            method: fc.constant('updateTask'),
            status: fc.constant(404),
            hasValidationError: fc.constant(false),
            taskId: taskIdArb,
            updateData: updateDataArb,
          }),
          // Test updateTask with other errors
          fc.record({
            method: fc.constant('updateTask'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
            taskId: taskIdArb,
            updateData: updateDataArb,
          }),
          // Test deleteTask with non-404 errors (404 is handled gracefully)
          fc.record({
            method: fc.constant('deleteTask'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
            taskId: taskIdArb,
          }),
          // Test deleteAllTasks with errors
          fc.record({
            method: fc.constant('deleteAllTasks'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
          }),
          // Test getTaskById with 404 errors
          fc.record({
            method: fc.constant('getTaskById'),
            status: fc.constant(404),
            hasValidationError: fc.constant(false),
            taskId: taskIdArb,
          }),
          // Test getTaskById with other errors
          fc.record({
            method: fc.constant('getTaskById'),
            status: httpErrorStatusArb,
            hasValidationError: fc.constant(false),
            taskId: taskIdArb,
          })
        ),
        async (testCase) => {
          // Mock fetch to return error response
          global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            status: testCase.status,
            json: async () => (testCase.hasValidationError ? testCase.validationError : {}),
          });

          let thrownError = null;

          try {
            // Call the appropriate API method
            switch (testCase.method) {
              case 'getAllTasks':
                await taskApi.getAllTasks();
                break;
              case 'createTask':
                await taskApi.createTask(testCase.taskData);
                break;
              case 'updateTask':
                await taskApi.updateTask(testCase.taskId, testCase.updateData);
                break;
              case 'deleteTask':
                await taskApi.deleteTask(testCase.taskId);
                break;
              case 'deleteAllTasks':
                await taskApi.deleteAllTasks();
                break;
              case 'getTaskById':
                await taskApi.getTaskById(testCase.taskId);
                break;
            }
          } catch (error) {
            thrownError = error;
          }

          // Property: All failed operations should throw an Error with a message
          expect(thrownError).toBeInstanceOf(Error);
          expect(thrownError.message).toBeTruthy();
          expect(typeof thrownError.message).toBe('string');
          expect(thrownError.message.length).toBeGreaterThan(0);

          // Additional consistency check: error messages should be meaningful
          // (not just empty strings or whitespace)
          expect(thrownError.message.trim().length).toBeGreaterThan(0);
        }
      ),
      { numRuns: 100 } // Run 100 iterations as specified in design doc
    );
  });

  /**
   * Edge case: deleteTask with 404 should NOT throw an error
   * This is a special case where 404 is handled gracefully
   */
  it('Edge case: deleteTask with 404 returns gracefully without error', async () => {
    await fc.assert(
      fc.asyncProperty(fc.uuid(), async (taskId) => {
        // Mock fetch to return 404
        global.fetch = vi.fn().mockResolvedValue({
          ok: false,
          status: 404,
          json: async () => ({}),
        });

        // Should not throw
        await expect(taskApi.deleteTask(taskId)).resolves.toBeUndefined();
      }),
      { numRuns: 100 }
    );
  });

  /**
   * Unit test for deleteAllTasks API method
   */
  describe('deleteAllTasks method', () => {
    it('should make DELETE request to /api/tasks', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 204,
      });
      global.fetch = mockFetch;

      await taskApi.deleteAllTasks();

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tasks'),
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });

    it('should return void on successful deletion', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 204,
      });

      const result = await taskApi.deleteAllTasks();

      expect(result).toBeUndefined();
    });

    it('should throw error on failed deletion', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
      });

      await expect(taskApi.deleteAllTasks()).rejects.toThrow(/HTTP error! status: 500/);
    });
  });
});
