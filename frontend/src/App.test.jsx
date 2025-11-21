import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
    // Reset fetch mock
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Initial Render', () => {
    it('should render the main heading', () => {
      render(<App />);
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 });
      expect(heading).toBeInTheDocument();
    });

    it('should render the subtitle', () => {
      render(<App />);
      const subtitle = screen.getByText(/fullstack demo application/i);
      expect(subtitle).toBeInTheDocument();
    });

    it('should render the button with correct initial text', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toBeInTheDocument();
      expect(button).not.toBeDisabled();
    });

    it('should not display any message, error, or loading state initially', () => {
      render(<App />);
      expect(screen.queryByText(/connecting to backend/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/response from backend/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/failed to connect/i)).not.toBeInTheDocument();
    });
  });

  describe('Button Interactions', () => {
    it('should show loading state when button is clicked', async () => {
      const user = userEvent.setup();
      
      // Mock a pending fetch
      global.fetch = vi.fn(() => new Promise(() => {}));
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      expect(screen.getByText(/connecting to backend/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /loading/i })).toBeDisabled();
    });

    it('should disable button during loading', async () => {
      const user = userEvent.setup();
      
      // Mock a pending fetch
      global.fetch = vi.fn(() => new Promise(() => {}));
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      expect(button).toBeDisabled();
      expect(button).toHaveTextContent(/loading/i);
    });
  });

  describe('Successful API Call', () => {
    it('should display message from backend on successful fetch', async () => {
      const user = userEvent.setup();
      const mockData = {
        message: 'Hello from Backend!',
        timestamp: '2024-01-01T12:00:00Z'
      };

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      );

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/response from backend/i)).toBeInTheDocument();
      });

      expect(screen.getByText(/hello from backend!/i)).toBeInTheDocument();
      expect(screen.getByText(/received at: 2024-01-01t12:00:00z/i)).toBeInTheDocument();
    });

    it('should call fetch with correct URL', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello');
      });
    });

    it('should clear previous state before new fetch', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'New Message', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      // First click
      await user.click(button);
      await waitFor(() => {
        expect(screen.getByText(/new message/i)).toBeInTheDocument();
      });

      // Second click should clear previous message during loading
      global.fetch = vi.fn(() => new Promise(() => {})); // pending promise
      await user.click(button);
      
      expect(screen.getByText(/connecting to backend/i)).toBeInTheDocument();
    });

    it('should remove loading state after successful fetch', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/connecting to backend/i)).not.toBeInTheDocument();
      });

      expect(button).not.toBeDisabled();
      expect(button).toHaveTextContent(/get message from backend/i);
    });
  });

  describe('Failed API Call', () => {
    it('should display error message when fetch fails with non-ok response', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500
        })
      );

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });

      expect(screen.getByText(/make sure the backend server is running on port 8000/i)).toBeInTheDocument();
    });

    it('should display error message when fetch throws network error', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });
    });

    it('should display error icon with error message', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        const errorDiv = screen.getByText(/failed to connect to backend/i).closest('div');
        expect(errorDiv).toHaveTextContent('❌');
      });
    });

    it('should remove loading state after error', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/connecting to backend/i)).not.toBeInTheDocument();
      });

      expect(button).not.toBeDisabled();
      expect(button).toHaveTextContent(/get message from backend/i);
    });

    it('should not display success message when error occurs', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });

      expect(screen.queryByText(/response from backend/i)).not.toBeInTheDocument();
    });
  });

  describe('State Management', () => {
    it('should handle multiple rapid clicks correctly', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      // Click multiple times
      await user.click(button);
      await user.click(button);
      await user.click(button);

      // Wait for the last request to complete
      await waitFor(() => {
        expect(screen.getByText(/response from backend/i)).toBeInTheDocument();
      });

      // Fetch should have been called for each click
      expect(global.fetch).toHaveBeenCalled();
    });

    it('should clear error message on new successful fetch', async () => {
      const user = userEvent.setup();
      
      // First fetch fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });

      // Second fetch succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success', timestamp: '2024-01-01' })
        })
      );

      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/failed to connect to backend/i)).not.toBeInTheDocument();
      });

      expect(screen.getByText(/response from backend/i)).toBeInTheDocument();
    });

    it('should clear success message on new failed fetch', async () => {
      const user = userEvent.setup();
      
      // First fetch succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(/response from backend/i)).toBeInTheDocument();
      });

      // Second fetch fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      await user.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/response from backend/i)).not.toBeInTheDocument();
      });

      expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
    });
  });

  describe('Component Structure', () => {
    it('should have correct CSS class names', () => {
      const { container } = render(<App />);
      
      expect(container.querySelector('.app')).toBeInTheDocument();
      expect(container.querySelector('.container')).toBeInTheDocument();
      expect(container.querySelector('.title')).toBeInTheDocument();
      expect(container.querySelector('.subtitle')).toBeInTheDocument();
      expect(container.querySelector('.button')).toBeInTheDocument();
    });

    it('should render error message with correct CSS class', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

      const { container } = render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(container.querySelector('.error')).toBeInTheDocument();
      });
    });

    it('should render success message with correct CSS class', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test', timestamp: '2024-01-01' })
        })
      );

      const { container } = render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(container.querySelector('.message-box')).toBeInTheDocument();
      });
    });

    it('should render loading indicator with correct CSS class', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => new Promise(() => {}));

      const { container } = render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      expect(container.querySelector('.loading')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have accessible button element', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toBeInTheDocument();
    });

    it('should have accessible heading elements', () => {
      render(<App />);
      const mainHeading = screen.getByRole('heading', { name: /hello world/i, level: 1 });
      expect(mainHeading).toBeInTheDocument();
    });

    it('should communicate button state through text change', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() => new Promise(() => {}));

      render(<App />);
      const button = screen.getByRole('button');
      
      expect(button).toHaveTextContent(/get message from backend/i);
      
      await user.click(button);
      
      expect(button).toHaveTextContent(/loading/i);
    });

    it('should display success message heading when data is loaded', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test', timestamp: '2024-01-01' })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        const responseHeading = screen.getByRole('heading', { name: /response from backend/i, level: 3 });
        expect(responseHeading).toBeInTheDocument();
      });
    });
  });

  describe('JSON Response Handling', () => {
    it('should correctly parse and display JSON response with message and timestamp', async () => {
      const user = userEvent.setup();
      const mockTimestamp = '2024-03-15T10:30:45.123Z';
      const mockMessage = 'Hello from the backend API!';
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ 
            message: mockMessage, 
            timestamp: mockTimestamp 
          })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        expect(screen.getByText(new RegExp(mockMessage, 'i'))).toBeInTheDocument();
        expect(screen.getByText(new RegExp(mockTimestamp, 'i'))).toBeInTheDocument();
      });
    });

    it('should format the complete message with timestamp correctly', async () => {
      const user = userEvent.setup();
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ 
            message: 'Test Message', 
            timestamp: '2024-01-01T00:00:00Z' 
          })
        })
      );

      render(<App />);
      const button = screen.getByRole('button');
      
      await user.click(button);

      await waitFor(() => {
        const fullMessage = screen.getByText(/test message \(received at: 2024-01-01t00:00:00z\)/i);
        expect(fullMessage).toBeInTheDocument();
      });
    });
  });
});
