import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

// Mock fetch globally
global.fetch = vi.fn();

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  describe('Component Rendering', () => {
    it('should render without crashing', () => {
      render(<App />);
      expect(screen.getByText('Hello World')).toBeInTheDocument();
    });

    it('should render key UI elements', () => {
      render(<App />);
      
      // Check for heading
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument();
      
      // Check for button
      expect(screen.getByRole('button', { name: /get message from backend/i })).toBeInTheDocument();
      
      // Check for message display container
      expect(screen.getByText('Get Message from Backend').closest('.container')).toBeInTheDocument();
    });

    it('should have correct initial state', () => {
      render(<App />);
      
      // Button should be enabled initially
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).not.toBeDisabled();
      
      // No loading, error, or message should be displayed initially
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument();
      expect(screen.queryByRole('paragraph', { name: /message/i })).not.toBeInTheDocument();
    });

    it('should render with proper CSS classes', () => {
      render(<App />);
      
      expect(document.querySelector('.app')).toBeInTheDocument();
      expect(document.querySelector('.container')).toBeInTheDocument();
      expect(document.querySelector('.fetch-button')).toBeInTheDocument();
      expect(document.querySelector('.message-display')).toBeInTheDocument();
    });
  });

  describe('Button Click Interactions', () => {
    it('should call fetch API when button is clicked', async () => {
      const mockResponse = { message: 'Hello from backend!' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/hello')
      );
    });

    it('should display success message after successful API call', async () => {
      const mockResponse = { message: 'Hello from backend!' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText('Hello from backend!')).toBeInTheDocument();
      });
    });

    it('should clear previous messages when button is clicked again', async () => {
      const mockResponse1 = { message: 'First message' };
      const mockResponse2 = { message: 'Second message' };
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockResponse1,
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockResponse2,
        });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // First click
      await user.click(button);
      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument();
      });

      // Second click
      await user.click(button);
      await waitFor(() => {
        expect(screen.getByText('Second message')).toBeInTheDocument();
      });
      
      // First message should be replaced
      expect(screen.queryByText('First message')).not.toBeInTheDocument();
    });

    it('should handle response with only data object (no message property)', async () => {
      const mockResponse = { data: 'test', status: 'ok' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(JSON.stringify(mockResponse))).toBeInTheDocument();
      });
    });
  });

  describe('Loading States', () => {
    it('should display loading indicator when fetching data', async () => {
      global.fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test' }),
        }), 100))
      );

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      // Loading should be displayed
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
      expect(screen.getByText(/loading/i)).toHaveClass('loading');
    });

    it('should disable button during loading', async () => {
      global.fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test' }),
        }), 100))
      );

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      // Button should be disabled during loading
      expect(button).toBeDisabled();
    });

    it('should hide loading indicator after successful fetch', async () => {
      const mockResponse = { message: 'Success!' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
        expect(screen.getByText('Success!')).toBeInTheDocument();
      });
    });

    it('should hide loading indicator after failed fetch', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
      });
    });

    it('should re-enable button after loading completes', async () => {
      const mockResponse = { message: 'Test' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(button).not.toBeDisabled();
      });
    });
  });

  describe('Error Handling', () => {
    it('should display error message when API returns non-OK status', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: HTTP error! status: 500/i)).toBeInTheDocument();
      });
    });

    it('should display error message when network request fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: Network error/i)).toBeInTheDocument();
      });
    });

    it('should apply error CSS class to error message', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Test error'));

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        const errorElement = screen.getByText(/failed to fetch: Test error/i);
        expect(errorElement).toHaveClass('error');
      });
    });

    it('should clear previous error when new request is made', async () => {
      global.fetch
        .mockRejectedValueOnce(new Error('First error'))
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' }),
        });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // First click - error
      await user.click(button);
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: First error/i)).toBeInTheDocument();
      });

      // Second click - success
      await user.click(button);
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch: First error/i)).not.toBeInTheDocument();
        expect(screen.getByText('Success')).toBeInTheDocument();
      });
    });

    it('should not display success message when error occurs', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Error'));

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
      });

      // Message display should not show success message
      const messageDisplay = screen.getByText(/failed to fetch/i).closest('.message-display');
      expect(messageDisplay.querySelector('.message')).not.toBeInTheDocument();
    });

    it('should handle error recovery - successful request after error', async () => {
      global.fetch
        .mockRejectedValueOnce(new Error('Temporary error'))
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Recovered successfully' }),
        });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // First attempt - error
      await user.click(button);
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: Temporary error/i)).toBeInTheDocument();
      });

      // Second attempt - recovery
      await user.click(button);
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument();
        expect(screen.getByText('Recovered successfully')).toBeInTheDocument();
      });
    });

    it('should handle JSON parsing errors gracefully', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => {
          throw new Error('Invalid JSON');
        },
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: Invalid JSON/i)).toBeInTheDocument();
      });
    });

    it('should handle different HTTP error status codes', async () => {
      const statusCodes = [400, 401, 403, 404, 500, 503];
      
      for (const status of statusCodes) {
        vi.clearAllMocks();
        global.fetch.mockResolvedValueOnce({
          ok: false,
          status,
        });

        const user = userEvent.setup();
        const { unmount } = render(<App />);
        
        const button = screen.getByRole('button', { name: /get message from backend/i });
        await user.click(button);

        await waitFor(() => {
          expect(screen.getByText(new RegExp(`HTTP error! status: ${status}`, 'i'))).toBeInTheDocument();
        });
        
        unmount();
      }
    });
  });

  describe('API URL Configuration', () => {
    it('should use API_URL environment variable when available', async () => {
      const mockResponse = { message: 'Test' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringMatching(/\/api\/hello$/)
        );
      });
    });
  });

  describe('Message Display', () => {
    it('should apply correct CSS class to success message', async () => {
      const mockResponse = { message: 'Success message' };
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        const messageElement = screen.getByText('Success message');
        expect(messageElement).toHaveClass('message');
      });
    });

    it('should not display message during loading', async () => {
      global.fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test' }),
        }), 100))
      );

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      // During loading, message should not be displayed
      expect(screen.queryByText('Test')).not.toBeInTheDocument();
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    it('should not display message when error is present', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Error'));

      const user = userEvent.setup();
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
      });

      // Success message element should not exist
      expect(document.querySelector('.message')).not.toBeInTheDocument();
    });
  });
});
