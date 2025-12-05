/**
 * Tests for API Service Module
 * Covers all task-related API methods including delete all functionality
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { taskApi } from './api';

// Mock fetch globally
global.fetch = vi.fn();

describe('taskApi', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  describe('getAllTasks', () => {
    it('should fetch all tasks successfully', async () => {
      const mockTasks = {
        tasks: [
          {
            id: '1',
            title: 'Test Task',
            description: 'Test Description',
            completed: false,
          },
        ],
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTasks,
      });

      const result = await taskApi.getAllTasks();

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks'
      );
      expect(result).toEqual(mockTasks);
    });

    it('should throw error when fetch fails', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      await expect(taskApi.getAllTasks()).rejects.toThrow(
        'HTTP error! status: 500'
      );
    });
  });

  describe('createTask', () => {
    it('should create a task successfully', async () => {
      const taskData = {
        title: 'New Task',
        description: 'New Description',
      };
      const mockResponse = {
        id: '1',
        ...taskData,
        completed: false,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await taskApi.createTask(taskData);

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(taskData),
        }
      );
      expect(result).toEqual(mockResponse);
    });

    it('should handle validation error (422)', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 422,
        json: async () => ({
          detail: [{ msg: 'Title cannot be empty' }],
        }),
      });

      await expect(
        taskApi.createTask({ title: '' })
      ).rejects.toThrow('Title cannot be empty');
    });
  });

  describe('updateTask', () => {
    it('should update a task successfully', async () => {
      const taskId = '1';
      const taskData = { title: 'Updated Title' };
      const mockResponse = {
        id: taskId,
        ...taskData,
        completed: false,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await taskApi.updateTask(taskId, taskData);

      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/tasks/${taskId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(taskData),
        }
      );
      expect(result).toEqual(mockResponse);
    });

    it('should handle task not found (404)', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      await expect(
        taskApi.updateTask('999', { title: 'Test' })
      ).rejects.toThrow('Task not found. It may have been deleted.');
    });
  });

  describe('deleteTask', () => {
    it('should delete a task successfully', async () => {
      const taskId = '1';

      global.fetch.mockResolvedValueOnce({
        ok: true,
      });

      await taskApi.deleteTask(taskId);

      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/tasks/${taskId}`,
        {
          method: 'DELETE',
        }
      );
    });

    it('should handle 404 gracefully', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      // Should not throw error for 404
      await expect(taskApi.deleteTask('999')).resolves.toBeUndefined();
    });

    it('should throw error for other failures', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      await expect(taskApi.deleteTask('1')).rejects.toThrow(
        'HTTP error! status: 500'
      );
    });
  });

  describe('deleteAllTasks', () => {
    it('should delete all tasks successfully', async () => {
      const mockResponse = {
        success: true,
        message: 'All tasks deleted successfully',
        deletedCount: 5,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await taskApi.deleteAllTasks();

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks/all',
        {
          method: 'DELETE',
        }
      );
      expect(result).toEqual(mockResponse);
    });

    it('should delete zero tasks when list is empty', async () => {
      const mockResponse = {
        success: true,
        message: 'All tasks deleted successfully',
        deletedCount: 0,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await taskApi.deleteAllTasks();

      expect(result).toEqual(mockResponse);
      expect(result.deletedCount).toBe(0);
    });

    it('should handle server error (500)', async () => {
      const mockErrorResponse = {
        detail: {
          success: false,
          message: 'Error deleting tasks',
          error: 'Database connection failed',
        },
      };

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => mockErrorResponse,
      });

      await expect(taskApi.deleteAllTasks()).rejects.toThrow(
        'Database connection failed'
      );
    });

    it('should handle network error', async () => {
      global.fetch.mockRejectedValueOnce(
        new Error('Network request failed')
      );

      await expect(taskApi.deleteAllTasks()).rejects.toThrow(
        'Network request failed'
      );
    });

    it('should use correct endpoint /api/tasks/all', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          success: true,
          message: 'All tasks deleted successfully',
          deletedCount: 3,
        }),
      });

      await taskApi.deleteAllTasks();

      const fetchCall = global.fetch.mock.calls[0];
      expect(fetchCall[0]).toBe('http://localhost:8000/api/tasks/all');
    });
  });

  describe('getTaskById', () => {
    it('should get a task by ID successfully', async () => {
      const taskId = '1';
      const mockTask = {
        id: taskId,
        title: 'Test Task',
        description: 'Test Description',
        completed: false,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTask,
      });

      const result = await taskApi.getTaskById(taskId);

      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/tasks/${taskId}`
      );
      expect(result).toEqual(mockTask);
    });

    it('should handle task not found (404)', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      await expect(taskApi.getTaskById('999')).rejects.toThrow(
        'Task not found'
      );
    });
  });
});
