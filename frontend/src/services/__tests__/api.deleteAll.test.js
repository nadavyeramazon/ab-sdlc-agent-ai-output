import { describe, it, expect, beforeEach, vi } from 'vitest';
import { taskApi } from '../services/api';

// Mock fetch globally
global.fetch = vi.fn();

describe('taskApi.deleteAllTasks', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should make DELETE request to /api/tasks', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await taskApi.deleteAllTasks();

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/tasks'),
      expect.objectContaining({
        method: 'DELETE',
      })
    );
  });

  it('should handle successful deletion (204 No Content)', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await expect(taskApi.deleteAllTasks()).resolves.toBeUndefined();
  });

  it('should throw error when API returns error status', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 500,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 500'
    );
  });

  it('should throw error when API returns 403 Forbidden', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 403,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 403'
    );
  });

  it('should handle network errors', async () => {
    global.fetch.mockRejectedValue(new Error('Network connection failed'));

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'Network connection failed'
    );
  });

  it('should use correct API URL from constants', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await taskApi.deleteAllTasks();

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/tasks'),
      expect.any(Object)
    );
  });

  it('should not include request body', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await taskApi.deleteAllTasks();

    const callArgs = global.fetch.mock.calls[0];
    expect(callArgs[1].body).toBeUndefined();
  });

  it('should handle 404 Not Found error', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 404,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 404'
    );
  });

  it('should handle timeout errors', async () => {
    global.fetch.mockImplementation(
      () =>
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Request timeout')), 100)
        )
    );

    await expect(taskApi.deleteAllTasks()).rejects.toThrow('Request timeout');
  });

  it('should throw error for 401 Unauthorized', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 401,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 401'
    );
  });

  it('should throw error for 400 Bad Request', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 400,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 400'
    );
  });

  it('should make exactly one API call', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await taskApi.deleteAllTasks();

    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  it('should use DELETE method (case-sensitive)', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    await taskApi.deleteAllTasks();

    const callArgs = global.fetch.mock.calls[0];
    expect(callArgs[1].method).toBe('DELETE');
  });

  it('should handle 503 Service Unavailable', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 503,
    });

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'HTTP error! status: 503'
    );
  });

  it('should handle CORS errors', async () => {
    global.fetch.mockRejectedValue(
      new Error('Failed to fetch: CORS policy blocked')
    );

    await expect(taskApi.deleteAllTasks()).rejects.toThrow(
      'Failed to fetch: CORS policy blocked'
    );
  });

  it('should return void on success', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 204,
    });

    const result = await taskApi.deleteAllTasks();

    expect(result).toBeUndefined();
  });
});
