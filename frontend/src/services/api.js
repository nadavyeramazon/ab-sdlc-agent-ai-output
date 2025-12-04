/**
 * API Service Module
 * Centralizes all HTTP communication with the backend API
 */

import { API_URL } from '../utils/constants.js';

/**
 * Task API service object containing all task-related API methods
 */
export const taskApi = {
  /**
   * Retrieve all tasks from the backend
   * @returns {Promise<Object>} Object containing tasks array
   * @throws {Error} If the request fails
   */
  async getAllTasks() {
    const response = await fetch(`${API_URL}/api/tasks`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  /**
   * Create a new task
   * @param {Object} taskData - Task data containing title and optional description
   * @param {string} taskData.title - Task title (required)
   * @param {string} [taskData.description] - Task description (optional)
   * @returns {Promise<Object>} The created task object
   * @throws {Error} If validation fails or request fails
   */
  async createTask(taskData) {
    const response = await fetch(`${API_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 422) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.[0]?.msg || 'Validation error');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  /**
   * Update an existing task
   * @param {string} taskId - ID of the task to update
   * @param {Object} taskData - Updated task data
   * @param {string} [taskData.title] - Updated title
   * @param {string} [taskData.description] - Updated description
   * @param {boolean} [taskData.completed] - Updated completion status
   * @returns {Promise<Object>} The updated task object
   * @throws {Error} If task not found, validation fails, or request fails
   */
  async updateTask(taskId, taskData) {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 422) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.[0]?.msg || 'Validation error');
      }
      if (response.status === 404) {
        throw new Error('Task not found. It may have been deleted.');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  /**
   * Delete a task
   * @param {string} taskId - ID of the task to delete
   * @returns {Promise<void>}
   * @throws {Error} If request fails (404 errors are handled gracefully)
   */
  async deleteTask(taskId) {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      if (response.status === 404) {
        // Task already deleted, return gracefully
        return;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  },

  /**
   * Delete all tasks
   * @returns {Promise<null>}
   * @throws {Error} If request fails
   */
  async deleteAllTasks() {
    const response = await fetch(`${API_URL}/api/tasks`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 204 No Content - no body to parse
    return null;
  },

  /**
   * Get a single task by ID
   * @param {string} taskId - ID of the task to retrieve
   * @returns {Promise<Object>} The task object
   * @throws {Error} If task not found or request fails
   */
  async getTaskById(taskId) {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },
};
