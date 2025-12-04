/**
 * Application Constants
 * Centralized location for shared constants used across the application
 */

/**
 * Base URL for the backend API
 * Defaults to localhost:8000 if VITE_API_URL environment variable is not set
 */
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
