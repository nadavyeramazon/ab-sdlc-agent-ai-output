import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { act } from 'react';
import { useTasks } from '../useTasks';
import { taskApi } from '../../services/api';

// Mock the taskApi module
vi.mock('../../services/api', () => ({
  taskApi: {
    getAllTasks: vi.fn(),
    createTask: vi.fn(),
    updateTask: vi.fn(),
    deleteTask: vi.fn(),
    deleteAllTasks: vi.fn(),
  },
}));

describe('useTasks Hook - deleteAllTasks', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Default mock for getAllTasks (called on mount)
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });
  });

  describe('deleteAllTasks function', () => {
    it('should be available in the hook return value', async () => {
      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.deleteAllTasks).toBeDefined();
      expect(typeof result.current.deleteAllTasks).toBe('function');
    });

    it('should call taskApi.deleteAllTasks when invoked', async () => {
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      await act(async () => {
        await result.current.deleteAllTasks();
      });

      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);
    });

    it('should clear local tasks state on success', async () => {
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

      taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(2);
      });

      expect(result.current.tasks).toEqual(mockTasks);

      // Delete all tasks
      await act(async () => {
        await result.current.deleteAllTasks();
      });

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(0);
      });

      expect(result.current.tasks).toEqual([]);
    });

    it('should return true on successful deletion', async () => {
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(true);
    });

    it('should return false on failed deletion', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('Failed to delete tasks')
      );

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);
    });

    it('should set error state when deletion fails', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('Server error occurred')
      );

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.error).toBeNull();

      await act(async () => {
        await result.current.deleteAllTasks();
      });

      await waitFor(() => {
        expect(result.current.error).toBe('Server error occurred');
      });
    });

    it('should clear error state before deletion attempt', async () => {
      // First, create an error state
      taskApi.createTask.mockRejectedValue(new Error('Previous error'));

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Create an error
      await act(async () => {
        await result.current.createTask({ title: 'Test' });
      });

      await waitFor(() => {
        expect(result.current.error).toBe('Previous error');
      });

      // Now attempt deleteAllTasks (which will succeed)
      taskApi.deleteAllTasks.mockResolvedValue(undefined);
      await act(async () => {
        await result.current.deleteAllTasks();
      });

      await waitFor(() => {
        expect(result.current.error).toBeNull();
      });
    });

    it('should handle network errors', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('Network connection failed')
      );

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);

      await waitFor(() => {
        expect(result.current.error).toBe('Network connection failed');
      });
    });

    it('should handle 500 Internal Server Error', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('HTTP error! status: 500')
      );

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);

      await waitFor(() => {
        expect(result.current.error).toBe('HTTP error! status: 500');
      });
    });

    it('should handle 403 Forbidden error', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(
        new Error('HTTP error! status: 403')
      );

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);

      await waitFor(() => {
        expect(result.current.error).toBe('HTTP error! status: 403');
      });
    });

    it('should not affect other tasks operations', async () => {
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

      taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(1);
      });

      // Verify other operations are still available
      expect(result.current.createTask).toBeDefined();
      expect(result.current.updateTask).toBeDefined();
      expect(result.current.deleteTask).toBeDefined();
      expect(result.current.toggleTaskComplete).toBeDefined();
      expect(result.current.fetchTasks).toBeDefined();

      // Delete all tasks
      await act(async () => {
        await result.current.deleteAllTasks();
      });

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(0);
      });

      // Verify operations are still available after deleteAll
      expect(result.current.createTask).toBeDefined();
      expect(result.current.updateTask).toBeDefined();
      expect(result.current.deleteTask).toBeDefined();
    });

    it('should be callable multiple times', async () => {
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Call deleteAllTasks multiple times
      await act(async () => {
        await result.current.deleteAllTasks();
      });
      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);

      await act(async () => {
        await result.current.deleteAllTasks();
      });
      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(2);

      await act(async () => {
        await result.current.deleteAllTasks();
      });
      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(3);
    });

    it('should clear tasks even when starting with empty list', async () => {
      taskApi.getAllTasks.mockResolvedValue({ tasks: [] });
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.tasks).toHaveLength(0);

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(true);
      expect(result.current.tasks).toHaveLength(0);
    });

    it('should handle concurrent deleteAllTasks calls', async () => {
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

      taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(1);
      });

      // Make concurrent calls
      let success1, success2;
      await act(async () => {
        const promise1 = result.current.deleteAllTasks();
        const promise2 = result.current.deleteAllTasks();

        [success1, success2] = await Promise.all([promise1, promise2]);
      });

      expect(success1).toBe(true);
      expect(success2).toBe(true);
      expect(result.current.tasks).toHaveLength(0);
    });

    it('should preserve tasks when API call fails', async () => {
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

      taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
      taskApi.deleteAllTasks.mockRejectedValue(new Error('Failed to delete'));

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(2);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);

      // Tasks should still be present in state (hook preserves tasks on error)
      expect(result.current.tasks).toHaveLength(2);
      expect(result.current.tasks).toEqual(mockTasks);
    });

    it('should handle timeout errors gracefully', async () => {
      taskApi.deleteAllTasks.mockRejectedValue(new Error('Request timeout'));

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(false);

      await waitFor(() => {
        expect(result.current.error).toBe('Request timeout');
      });
    });

    it('should pass no arguments to taskApi.deleteAllTasks', async () => {
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      await act(async () => {
        await result.current.deleteAllTasks();
      });

      expect(taskApi.deleteAllTasks).toHaveBeenCalledWith();
    });

    it('should work correctly after other operations', async () => {
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

      taskApi.getAllTasks.mockResolvedValue({ tasks: mockTasks });
      taskApi.updateTask.mockResolvedValue({
        ...mockTasks[0],
        completed: true,
        updated_at: new Date().toISOString(),
      });
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(1);
      });

      // Update a task first
      await act(async () => {
        await result.current.updateTask('1', { completed: true });
      });

      await waitFor(() => {
        expect(result.current.tasks[0].completed).toBe(true);
      });

      // Then delete all tasks
      let success;
      await act(async () => {
        success = await result.current.deleteAllTasks();
      });

      expect(success).toBe(true);
      expect(result.current.tasks).toHaveLength(0);
    });
  });

  describe('Integration with other hook methods', () => {
    it('should work alongside createTask', async () => {
      const newTask = {
        id: '1',
        title: 'New Task',
        description: 'New Description',
        completed: false,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };

      taskApi.createTask.mockResolvedValue(newTask);
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Create a task
      await act(async () => {
        await result.current.createTask({
          title: 'New Task',
          description: 'New Description',
        });
      });

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(1);
      });

      // Delete all tasks
      await act(async () => {
        await result.current.deleteAllTasks();
      });

      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(0);
      });
    });

    it('should not interfere with loading state', async () => {
      taskApi.deleteAllTasks.mockResolvedValue(undefined);

      const { result } = renderHook(() => useTasks());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // deleteAllTasks should not set loading to true (it's for initial fetch)
      await act(async () => {
        await result.current.deleteAllTasks();
      });

      expect(result.current.loading).toBe(false);
    });
  });
});
