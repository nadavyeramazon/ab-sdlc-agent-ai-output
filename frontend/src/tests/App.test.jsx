import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.resetAllMocks();
  });

  describe('Initial Rendering', () => {
    it('should render the main heading', () => {
      render(<App />);
      const heading = screen.getByRole('heading', { name: /hello world/i });
      expect(heading).toBeInTheDocument();
    });

    it('should render the fetch button', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toBeInTheDocument();
    });

    it('should not display any message initially', () => {
      render(<App />);
      expect(screen.queryByText(/backend says:/i)).not.toBeInTheDocument();
    });

    it('should not display loading indicator initially', () => {
      render(<App />);
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });

    it('should not display error message initially', () => {
      render(<App />);
      expect(screen.queryByText(/error:/i)).not.toBeInTheDocument();
    });

    it('should have an enabled button initially', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).not.toBeDisabled();
    });
  });

  describe('User Interactions', () => {
    it('should call fetch when button is clicked', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello from backend!' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello');
    });

    it('should disable button while loading', async () => {
      const user = userEvent.setup();
      
      // Create a promise that we can control
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });

      global.fetch.mockReturnValueOnce(promise);

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      // Button should be disabled during loading
      expect(button).toBeDisabled();

      // Resolve the promise to finish the test
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test' })
      });

      await waitFor(() => {
        expect(button).not.toBeDisabled();
      });
    });
  });

  describe('Loading State', () => {
    it('should display loading indicator during fetch', async () => {
      const user = userEvent.setup();
      
      // Create a promise that we can control
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });

      global.fetch.mockReturnValueOnce(promise);

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      // Loading indicator should appear
      expect(screen.getByText(/loading/i)).toBeInTheDocument();

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test' })
      });

      // Loading should disappear after fetch completes
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      });
    });

    it('should hide previous messages when loading', async () => {
      const user = userEvent.setup();
      
      // First successful fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      // Wait for first message to appear
      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument();
      });

      // Second fetch with controlled promise
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      global.fetch.mockReturnValueOnce(promise);

      await user.click(button);

      // Previous message should be hidden during loading
      expect(screen.queryByText(/first message/i)).not.toBeInTheDocument();

      // Resolve promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Second message' })
      });

      await waitFor(() => {
        expect(screen.getByText(/second message/i)).toBeInTheDocument();
      });
    });
  });

  describe('Success Scenarios', () => {
    it('should display backend message on successful fetch', async () => {
      const user = userEvent.setup();
      const mockMessage = 'Hello from the backend!';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: mockMessage })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/backend says:/i)).toBeInTheDocument();
        expect(screen.getByText(mockMessage)).toBeInTheDocument();
      });
    });

    it('should display message with correct structure', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        const messageContainer = screen.getByText(/backend says:/i).closest('.message');
        expect(messageContainer).toBeInTheDocument();
        expect(messageContainer).toHaveClass('message');
      });
    });

    it('should handle multiple successful fetches', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument();
      });

      // Second fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Second message' })
      });

      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/second message/i)).toBeInTheDocument();
        expect(screen.queryByText(/first message/i)).not.toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('should display error message when fetch fails with network error', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/network error/i)).toBeInTheDocument();
      });
    });

    it('should display error message when response is not ok (404)', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/failed to fetch: 404/i)).toBeInTheDocument();
      });
    });

    it('should display error message when response is not ok (500)', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/failed to fetch: 500/i)).toBeInTheDocument();
      });
    });

    it('should handle error without message', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockRejectedValueOnce({});

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });
    });

    it('should clear previous error on new fetch attempt', async () => {
      const user = userEvent.setup();
      
      // First fetch fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument();
      });

      // Second fetch succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success!' })
      });

      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/network error/i)).not.toBeInTheDocument();
        expect(screen.getByText(/success!/i)).toBeInTheDocument();
      });
    });

    it('should clear previous message on error', async () => {
      const user = userEvent.setup();
      
      // First fetch succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/success message/i)).toBeInTheDocument();
      });

      // Second fetch fails
      global.fetch.mockRejectedValueOnce(new Error('Error occurred'));

      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/success message/i)).not.toBeInTheDocument();
        expect(screen.getByText(/error occurred/i)).toBeInTheDocument();
      });
    });

    it('should display error with correct structure', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockRejectedValueOnce(new Error('Test error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        const errorContainer = screen.getByText(/error:/i).closest('.error');
        expect(errorContainer).toBeInTheDocument();
        expect(errorContainer).toHaveClass('error');
      });
    });
  });

  describe('State Management', () => {
    it('should not show loading and message simultaneously', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/test message/i)).toBeInTheDocument();
      });

      // Loading should not be present when message is shown
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });

    it('should not show loading and error simultaneously', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockRejectedValueOnce(new Error('Error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
      });

      // Loading should not be present when error is shown
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });

    it('should not show message and error simultaneously', async () => {
      const user = userEvent.setup();
      
      // First success
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/success/i)).toBeInTheDocument();
      });

      // Then error
      global.fetch.mockRejectedValueOnce(new Error('Error'));
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
      });

      // Success message should be gone
      expect(screen.queryByText(/backend says:/i)).not.toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle response with empty message', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: '' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/backend says:/i)).toBeInTheDocument();
      });
    });

    it('should handle JSON parsing errors gracefully', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => {
          throw new Error('Invalid JSON');
        }
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/invalid json/i)).toBeInTheDocument();
      });
    });

    it('should handle rapid consecutive clicks', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ message: 'Message' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // Click multiple times rapidly
      await user.click(button);
      await user.click(button);
      await user.click(button);

      // Should still work correctly
      await waitFor(() => {
        expect(screen.getByText(/message/i)).toBeInTheDocument();
      });

      // Fetch should have been called multiple times
      expect(global.fetch).toHaveBeenCalledTimes(3);
    });
  });

  describe('Accessibility', () => {
    it('should have proper button role', () => {
      render(<App />);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('should have proper heading role', () => {
      render(<App />);
      const heading = screen.getByRole('heading', { level: 1 });
      expect(heading).toBeInTheDocument();
      expect(heading).toHaveTextContent('Hello World');
    });

    it('should disable button during loading for accessibility', async () => {
      const user = userEvent.setup();
      
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });

      global.fetch.mockReturnValueOnce(promise);

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      // Button should be disabled and have the disabled attribute
      expect(button).toBeDisabled();
      expect(button).toHaveAttribute('disabled');

      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test' })
      });

      await waitFor(() => {
        expect(button).not.toBeDisabled();
      });
    });
  });
});
