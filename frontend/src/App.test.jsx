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
    fetch.mockClear();
  });

  describe('Initial Render', () => {
    it('should render the main heading', () => {
      render(<App />);
      expect(screen.getByRole('heading', { name: /hello world/i, level: 1 })).toBeInTheDocument();
    });

    it('should render the greeting section heading', () => {
      render(<App />);
      expect(screen.getByRole('heading', { name: /personalized greeting/i, level: 2 })).toBeInTheDocument();
    });

    it('should render "Get Message from Backend" button', () => {
      render(<App />);
      expect(screen.getByRole('button', { name: /get message from backend/i })).toBeInTheDocument();
    });

    it('should render name input field', () => {
      render(<App />);
      expect(screen.getByPlaceholderText(/enter your name/i)).toBeInTheDocument();
    });

    it('should render "Greet Me" button', () => {
      render(<App />);
      expect(screen.getByRole('button', { name: /greet me/i })).toBeInTheDocument();
    });

    it('should not show any messages initially', () => {
      render(<App />);
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/failed/i)).not.toBeInTheDocument();
    });
  });

  describe('Get Message from Backend Feature', () => {
    it('should display loading state when fetching message', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {})); // Never resolves
      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);
      
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    it('should fetch and display message successfully', async () => {
      const mockResponse = {
        message: 'Hello from Backend!',
        timestamp: '2024-01-01T12:00:00Z'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Hello from Backend! \(2024-01-01T12:00:00Z\)/i)).toBeInTheDocument();
      });
    });

    it('should call correct API endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-01' })
      });

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello');
      });
    });

    it('should display error message when fetch fails', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });
    });

    it('should display error when response is not ok', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });
    });

    it('should clear previous messages before new fetch', async () => {
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message', timestamp: '2024-01-01' })
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/First message/i)).toBeInTheDocument();
      });

      // Second fetch that fails
      fetch.mockRejectedValueOnce(new Error('Network error'));
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/First message/i)).not.toBeInTheDocument();
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });
    });
  });

  describe('Greeting Feature - Component Rendering', () => {
    it('should render name input with correct attributes', () => {
      render(<App />);
      const input = screen.getByPlaceholderText(/enter your name/i);
      
      expect(input).toHaveAttribute('type', 'text');
      expect(input).toHaveAttribute('aria-label', 'Your name');
      expect(input).not.toBeDisabled();
    });

    it('should update input value when user types', async () => {
      render(<App />);
      const input = screen.getByPlaceholderText(/enter your name/i);
      
      await userEvent.type(input, 'John Doe');
      
      expect(input).toHaveValue('John Doe');
    });
  });

  describe('Greeting Feature - Validation Logic', () => {
    it('should show validation error when name is empty', async () => {
      render(<App />);
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument();
      expect(fetch).not.toHaveBeenCalled();
    });

    it('should show validation error when name is only whitespace', async () => {
      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, '   ');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument();
      expect(fetch).not.toHaveBeenCalled();
    });

    it('should trim whitespace from name before sending', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, John!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, '  John  ');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'John' })
          })
        );
      });
    });
  });

  describe('Greeting Feature - API Calls', () => {
    it('should send POST request with correct headers and body', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Alice!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Alice');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: 'Alice' })
          }
        );
      });
    });

    it('should display greeting response on success', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Bob! Welcome!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Bob');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Hello, Bob! Welcome!/i)).toBeInTheDocument();
      });
    });

    it('should handle API error with detail message', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Name is too long' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'VeryLongNameThatExceedsLimit');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Name is too long/i)).toBeInTheDocument();
      });
    });

    it('should handle API error without detail message', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({})
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'John');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Failed to get greeting/i)).toBeInTheDocument();
      });
    });

    it('should handle network error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network connection failed'));

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Jane');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Network connection failed/i)).toBeInTheDocument();
      });
    });

    it('should handle error without message', async () => {
      fetch.mockRejectedValueOnce({ status: 500 }); // Error without message property

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Test');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Network error. Please try again./i)).toBeInTheDocument();
      });
    });
  });

  describe('Greeting Feature - Loading States', () => {
    it('should show loading state during greeting fetch', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {})); // Never resolves

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'TestUser');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      expect(screen.getByRole('button', { name: /loading/i })).toBeInTheDocument();
    });

    it('should disable input and button during loading', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {}));

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'TestUser');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      expect(input).toBeDisabled();
      expect(screen.getByRole('button', { name: /loading/i })).toBeDisabled();
    });

    it('should re-enable input and button after request completes', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'TestUser');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(input).not.toBeDisabled();
        expect(screen.getByRole('button', { name: /greet me/i })).not.toBeDisabled();
      });
    });
  });

  describe('Greeting Feature - State Management', () => {
    it('should clear previous greeting response before new request', async () => {
      // First successful greeting
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Alice!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Alice');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Hello, Alice!/i)).toBeInTheDocument();
      });

      // Clear input and enter new name
      await userEvent.clear(input);
      await userEvent.type(input, 'Bob');

      // Second greeting
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Bob!' })
      });

      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/Hello, Alice!/i)).not.toBeInTheDocument();
        expect(screen.getByText(/Hello, Bob!/i)).toBeInTheDocument();
      });
    });

    it('should clear previous greeting error before new request', async () => {
      // First request with validation error
      render(<App />);
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument();

      // Enter name for second request
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'John');

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, John!' })
      });

      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument();
        expect(screen.getByText(/Hello, John!/i)).toBeInTheDocument();
      });
    });
  });

  describe('Integration - Both Features', () => {
    it('should handle both features independently', async () => {
      // Test backend message feature
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Backend says hi!', timestamp: '2024-01-01' })
      });

      render(<App />);
      
      const backendButton = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(backendButton);

      await waitFor(() => {
        expect(screen.getByText(/Backend says hi!/i)).toBeInTheDocument();
      });

      // Test greeting feature
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, User!' })
      });

      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'User');
      
      const greetButton = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(greetButton);

      await waitFor(() => {
        expect(screen.getByText(/Hello, User!/i)).toBeInTheDocument();
        expect(screen.getByText(/Backend says hi!/i)).toBeInTheDocument();
      });
    });

    it('should maintain separate error states for each feature', async () => {
      render(<App />);
      
      // Fail backend message fetch
      fetch.mockRejectedValueOnce(new Error('Backend error'));
      const backendButton = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(backendButton);

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
      });

      // Fail greeting validation
      const greetButton = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(greetButton);

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument();
      expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle special characters in name', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, José-María!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'José-María');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'José-María' })
          })
        );
      });
    });

    it('should handle rapid consecutive clicks on backend button', async () => {
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-01' })
      });

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // Click multiple times rapidly
      await userEvent.click(button);
      await userEvent.click(button);
      await userEvent.click(button);

      // Should have made 3 API calls
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(3);
      });
    });

    it('should handle rapid consecutive clicks on greet button', async () => {
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ greeting: 'Hello!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Test');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      
      // Click multiple times rapidly
      await userEvent.click(button);
      await userEvent.click(button);

      // Should have made 2 API calls (validation passed)
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(2);
      });
    });

    it('should handle empty response from backend', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({})
      });

      render(<App />);
      
      const button = screen.getByRole('button', { name: /get message from backend/i });
      await userEvent.click(button);

      await waitFor(() => {
        // Should display undefined values without crashing
        expect(screen.getByText(/undefined \(undefined\)/i)).toBeInTheDocument();
      });
    });

    it('should handle malformed JSON in error response', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => {
          throw new Error('Invalid JSON');
        }
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      await userEvent.type(input, 'Test');
      
      const button = screen.getByRole('button', { name: /greet me/i });
      await userEvent.click(button);

      await waitFor(() => {
        expect(screen.getByText(/Invalid JSON/i)).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility', () => {
    it('should have accessible input label', () => {
      render(<App />);
      const input = screen.getByLabelText(/your name/i);
      expect(input).toBeInTheDocument();
    });

    it('should have all interactive elements as buttons', () => {
      render(<App />);
      const buttons = screen.getAllByRole('button');
      expect(buttons).toHaveLength(2);
    });

    it('should maintain focus management during interactions', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello!' })
      });

      render(<App />);
      
      const input = screen.getByPlaceholderText(/enter your name/i);
      const button = screen.getByRole('button', { name: /greet me/i });
      
      input.focus();
      expect(input).toHaveFocus();
      
      await userEvent.type(input, 'Test');
      await userEvent.click(button);

      // Button should be clickable without losing functionality
      await waitFor(() => {
        expect(screen.getByText(/Hello!/i)).toBeInTheDocument();
      });
    });
  });
});
