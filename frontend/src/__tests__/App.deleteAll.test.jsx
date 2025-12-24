/**
 * Integration tests for Delete All Tasks feature
 * Tests the complete user flow for bulk delete functionality
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';
import { taskApi } from '../services/api';

// Mock the API
vi.mock('../services/api', () => ({
  taskApi: {
    getAllTasks: vi.fn(),
    createTask: vi.fn(),
    updateTask: vi.fn(),
    deleteTask: vi.fn(),
    deleteAllTasks: vi.fn(),
  },
}));

describe('Delete All Tasks Feature', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  /**
   * Test: Delete All button is visible when tasks exist
   */
  it('shows Delete All Tasks button when tasks exist', async () => {
    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
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
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Delete All button should be visible
    expect(screen.getByText('Delete All Tasks')).toBeInTheDocument();
  });

  /**
   * Test: Delete All button is hidden when no tasks exist
   */
  it('hides Delete All Tasks button when no tasks exist', async () => {
    // Mock API to return empty tasks
    taskApi.getAllTasks.mockResolvedValue({ tasks: [] });

    render(<App />);

    // Wait for initial load
    await waitFor(() => {
      expect(screen.queryByText('Delete All Tasks')).not.toBeInTheDocument();
    });
  });

  /**
   * Test: Clicking Delete All shows confirmation dialog
   */
  it('shows confirmation dialog when Delete All button is clicked', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
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
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // Confirmation dialog should appear
    expect(
      screen.getByText('Are you sure you want to delete all 2 task(s)?')
    ).toBeInTheDocument();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
    expect(screen.getByText('Confirm Delete')).toBeInTheDocument();

    // Delete All button should be hidden
    expect(screen.queryByText('Delete All Tasks')).not.toBeInTheDocument();
  });

  /**
   * Test: Cancel button hides confirmation dialog
   */
  it('hides confirmation dialog when Cancel is clicked', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // Confirmation should appear
    expect(screen.getByText('Cancel')).toBeInTheDocument();

    // Click Cancel
    const cancelButton = screen.getByText('Cancel');
    await user.click(cancelButton);

    // Confirmation dialog should be hidden
    await waitFor(() => {
      expect(
        screen.queryByText('Are you sure you want to delete all 1 task(s)?')
      ).not.toBeInTheDocument();
    });

    // Delete All button should be visible again
    expect(screen.getByText('Delete All Tasks')).toBeInTheDocument();
  });

  /**
   * Test: Confirm Delete removes all tasks
   */
  it('deletes all tasks when Confirm Delete is clicked', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
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
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    // Mock deleteAllTasks to succeed
    taskApi.deleteAllTasks.mockResolvedValue();

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // Click Confirm Delete
    const confirmButton = screen.getByText('Confirm Delete');
    await user.click(confirmButton);

    // Verify API was called
    await waitFor(() => {
      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);
    });

    // Tasks should be removed from UI
    await waitFor(() => {
      expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
    });

    // Should show empty state
    expect(
      screen.getByText('No tasks yet. Create your first task above!')
    ).toBeInTheDocument();
  });

  /**
   * Test: Loading state during delete all operation
   */
  it('shows loading state during delete all operation', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    // Mock deleteAllTasks with delay
    taskApi.deleteAllTasks.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    );

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // Click Confirm Delete
    const confirmButton = screen.getByText('Confirm Delete');
    await user.click(confirmButton);

    // Should show loading text
    expect(screen.getByText('Deleting...')).toBeInTheDocument();

    // Buttons should be disabled during loading
    expect(screen.getByText('Deleting...')).toBeDisabled();
    expect(screen.getByText('Cancel')).toBeDisabled();

    // Wait for operation to complete
    await waitFor(
      () => {
        expect(screen.queryByText('Deleting...')).not.toBeInTheDocument();
      },
      { timeout: 200 }
    );
  });

  /**
   * Test: Error handling for delete all operation
   */
  it('handles error during delete all operation', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    // Mock deleteAllTasks to fail
    taskApi.deleteAllTasks.mockRejectedValue(new Error('Failed to delete all tasks'));

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // Click Confirm Delete
    const confirmButton = screen.getByText('Confirm Delete');
    await user.click(confirmButton);

    // Wait for error handling
    await waitFor(() => {
      expect(taskApi.deleteAllTasks).toHaveBeenCalledTimes(1);
    });

    // Task should still be visible (rollback)
    expect(screen.getByText('Task 1')).toBeInTheDocument();

    // Confirmation dialog should be closed
    await waitFor(() => {
      expect(
        screen.queryByText('Are you sure you want to delete all 1 task(s)?')
      ).not.toBeInTheDocument();
    });
  });

  /**
   * Test: No window.confirm() is used
   */
  it('uses inline confirmation instead of window.confirm()', async () => {
    const user = userEvent.setup();
    const confirmSpy = vi.spyOn(window, 'confirm');

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Task 1',
          description: 'Description 1',
          completed: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
    });

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByText('Delete All Tasks');
    await user.click(deleteAllButton);

    // window.confirm should NOT be called
    expect(confirmSpy).not.toHaveBeenCalled();

    // Instead, inline confirmation should be visible
    expect(
      screen.getByText('Are you sure you want to delete all 1 task(s)?')
    ).toBeInTheDocument();

    confirmSpy.mockRestore();
  });
});
