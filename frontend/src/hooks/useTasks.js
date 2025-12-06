/**
 * useTasks Hook
 * Custom hook for managing task state and operations
 * Provides centralized task management with loading states and error handling
 */

import { useState, useEffect } from 'react';
import { taskApi } from '../services/api';

/**
 * Custom hook for managing tasks
 * @returns {Object} Task state and operations
 */
export function useTasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [deleteAllLoading, setDeleteAllLoading] = useState(false);

  /**
   * Fetch all tasks from the backend
   */
  const fetchTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await taskApi.getAllTasks();
      setTasks(data.tasks || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Create a new task with optimistic update
   * @param {Object} taskData - Task data containing title and optional description
   * @returns {Promise<boolean>} True if successful, false otherwise
   */
  const createTask = async (taskData) => {
    setError(null);

    try {
      const newTask = await taskApi.createTask(taskData);
      // Optimistic update: add new task to the beginning of the list
      setTasks([newTask, ...tasks]);
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  /**
   * Update an existing task with optimistic update
   * @param {string} taskId - ID of the task to update
   * @param {Object} taskData - Updated task data
   * @returns {Promise<boolean>} True if successful, false otherwise
   */
  const updateTask = async (taskId, taskData) => {
    setError(null);

    // Store original tasks for rollback on error
    const originalTasks = [...tasks];

    // Optimistic update: update task in the list immediately
    setTasks(
      tasks.map((task) => (task.id === taskId ? { ...task, ...taskData } : task))
    );

    try {
      const updatedTask = await taskApi.updateTask(taskId, taskData);
      // Replace optimistic update with actual server response
      setTasks(
        tasks.map((task) => (task.id === taskId ? updatedTask : task))
      );
      return true;
    } catch (err) {
      // Rollback on error
      setTasks(originalTasks);
      setError(err.message);
      return false;
    }
  };

  /**
   * Delete a task with optimistic update
   * @param {string} taskId - ID of the task to delete
   * @returns {Promise<boolean>} True if successful, false otherwise
   */
  const deleteTask = async (taskId) => {
    setError(null);

    // Store original tasks for rollback on error
    const originalTasks = [...tasks];

    // Optimistic update: remove task from list immediately
    setTasks(tasks.filter((task) => task.id !== taskId));

    try {
      await taskApi.deleteTask(taskId);
      return true;
    } catch (err) {
      // Rollback on error (unless it's a 404, which means already deleted)
      if (!err.message.includes('404')) {
        setTasks(originalTasks);
      }
      setError(err.message);
      return false;
    }
  };

  /**
   * Delete all tasks
   * @returns {Promise<boolean>} True if successful, false otherwise
   */
  const deleteAllTasks = async () => {
    setDeleteAllLoading(true);
    setError(null);

    // Store original tasks for rollback on error
    const originalTasks = [...tasks];

    try {
      await taskApi.deleteAllTasks();
      setTasks([]);
      return true;
    } catch (err) {
      // Rollback on error - restore original tasks
      setTasks(originalTasks);
      setError(err.message);
      return false;
    } finally {
      setDeleteAllLoading(false);
    }
  };

  /**
   * Toggle task completion status
   * @param {string} taskId - ID of the task to toggle
   * @param {boolean} currentStatus - Current completion status
   * @returns {Promise<boolean>} True if successful, false otherwise
   */
  const toggleTaskComplete = async (taskId, currentStatus) => {
    return updateTask(taskId, { completed: !currentStatus });
  };

  // Fetch tasks on mount
  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskComplete,
    deleteAllTasks,
    deleteAllLoading,
  };
}
