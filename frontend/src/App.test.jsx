import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { taskApi } from './services/api';

// Mock the API service
vi.mock('./services/api', () => ({
  taskApi: {
    getAllTasks: vi.fn(),
    createTask: vi.fn(),
    updateTask: vi.fn(),
    deleteTask: vi.fn(),
    deleteAllTasks: vi.fn(),
  },
}));

describe('App Component - Delete All Tasks Feature', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should display Delete All button when tasks are present', async () => {
    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Test Task 1',
          description: 'Description 1',
          completed: false,
          created_at: new Date().toISOString(),
        },
        {
          id: '2',
          title: 'Test Task 2',
          description: 'Description 2',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ],
    });

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Check that Delete All button is present
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    expect(deleteAllButton).toBeInTheDocument();
  });

  it('should NOT display Delete All button when no tasks are present', async () => {
    // Mock API to return empty tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [],
    });

    render(<App />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });

    // Check that Delete All button is NOT present
    const deleteAllButton = screen.queryByRole('button', {
      name: 'Delete All Tasks',
    });
    expect(deleteAllButton).not.toBeInTheDocument();
  });

  it('should show confirmation dialog when Delete All button is clicked', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Test Task',
          description: 'Description',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ],
    });

    // Mock window.confirm
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(false);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that confirm was called with correct message
    expect(confirmSpy).toHaveBeenCalledWith(
      'Are you sure you want to delete all tasks? This action cannot be undone.'
    );
  });

  it('should NOT delete tasks when user cancels confirmation', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Test Task',
          description: 'Description',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ],
    });

    // Mock window.confirm to return false (user cancels)
    vi.spyOn(window, 'confirm').mockReturnValue(false);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that deleteAllTasks was NOT called
    expect(taskApi.deleteAllTasks).not.toHaveBeenCalled();
  });

  it('should delete all tasks and show success message when user confirms', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks initially
    taskApi.getAllTasks
      .mockResolvedValueOnce({
        tasks: [
          {
            id: '1',
            title: 'Test Task 1',
            description: 'Description 1',
            completed: false,
            created_at: new Date().toISOString(),
          },
          {
            id: '2',
            title: 'Test Task 2',
            description: 'Description 2',
            completed: false,
            created_at: new Date().toISOString(),
          },
        ],
      })
      .mockResolvedValueOnce({
        tasks: [],
      });

    // Mock deleteAllTasks to return success
    taskApi.deleteAllTasks.mockResolvedValue({
      success: true,
      message: 'All tasks deleted',
      deletedCount: 2,
    });

    // Mock window.confirm to return true (user confirms)
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that deleteAllTasks was called
    expect(taskApi.deleteAllTasks).toHaveBeenCalled();

    // Check that getAllTasks was called again to refresh
    await waitFor(() => {
      expect(taskApi.getAllTasks).toHaveBeenCalledTimes(2);
    });

    // Check that success message is displayed
    await waitFor(() => {
      expect(screen.getByText('Successfully deleted 2 tasks')).toBeInTheDocument();
    });
  });

  it('should show correct singular/plural message for deleted tasks', async () => {
    const user = userEvent.setup();

    // Mock API to return one task initially
    taskApi.getAllTasks
      .mockResolvedValueOnce({
        tasks: [
          {
            id: '1',
            title: 'Test Task',
            description: 'Description',
            completed: false,
            created_at: new Date().toISOString(),
          },
        ],
      })
      .mockResolvedValueOnce({
        tasks: [],
      });

    // Mock deleteAllTasks to return success with count 1
    taskApi.deleteAllTasks.mockResolvedValue({
      success: true,
      message: 'All tasks deleted',
      deletedCount: 1,
    });

    // Mock window.confirm to return true
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that success message uses singular form
    await waitFor(() => {
      expect(screen.getByText('Successfully deleted 1 task')).toBeInTheDocument();
    });
  });

  it('should show error message when delete all fails', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Test Task',
          description: 'Description',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ],
    });

    // Mock deleteAllTasks to throw error
    taskApi.deleteAllTasks.mockRejectedValue(new Error('Network error'));

    // Mock window.confirm to return true
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that error message is displayed
    await waitFor(() => {
      expect(
        screen.getByText(/Failed to delete all tasks: Network error/i)
      ).toBeInTheDocument();
    });
  });

  it('should disable Delete All button while deletion is in progress', async () => {
    const user = userEvent.setup();

    // Mock API to return tasks
    taskApi.getAllTasks.mockResolvedValue({
      tasks: [
        {
          id: '1',
          title: 'Test Task',
          description: 'Description',
          completed: false,
          created_at: new Date().toISOString(),
        },
      ],
    });

    // Mock deleteAllTasks with a delay
    taskApi.deleteAllTasks.mockImplementation(
      () =>
        new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              success: true,
              message: 'All tasks deleted',
              deletedCount: 1,
            });
          }, 100);
        })
    );

    // Mock window.confirm to return true
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    render(<App />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Click Delete All button
    const deleteAllButton = screen.getByRole('button', {
      name: 'Delete All Tasks',
    });
    await user.click(deleteAllButton);

    // Check that button shows loading state
    await waitFor(() => {
      expect(screen.getByText('Deleting...')).toBeInTheDocument();
    });

    // Check that button is disabled during loading
    const loadingButton = screen.getByRole('button', { name: 'Deleting...' });
    expect(loadingButton).toBeDisabled();
  });
});
