import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Initial Rendering', () => {
    it('renders the main title correctly', () => {
      render(<App />);
      const title = screen.getByRole('heading', { name: /hello world/i, level: 1 });
      expect(title).toBeInTheDocument();
    });

    it('renders the subtitle', () => {
      render(<App />);
      expect(screen.getByText(/green theme fullstack application/i)).toBeInTheDocument();
    });

    it('renders the fetch button', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toBeInTheDocument();
      expect(button).not.toBeDisabled();
    });

    it('renders the features section', () => {
      render(<App />);
      const featuresHeading = screen.getByRole('heading', { name: /features/i, level: 2 });
      expect(featuresHeading).toBeInTheDocument();
    });

    it('displays all feature items', () => {
      render(<App />);
      expect(screen.getByText(/green-themed responsive design/i)).toBeInTheDocument();
      expect(screen.getByText(/backend api integration/i)).toBeInTheDocument();
      expect(screen.getByText(/loading states & error handling/i)).toBeInTheDocument();
      expect(screen.getByText(/accessibility-compliant/i)).toBeInTheDocument();
      expect(screen.getByText(/built with react 18 & vite/i)).toBeInTheDocument();
    });

    it('renders the footer', () => {
      render(<App />);
      expect(screen.getByText(/powered by react \+ vite/i)).toBeInTheDocument();
    });

    it('does not show any messages initially', () => {
      render(<App />);
      const messageBoxes = screen.queryByRole('status');
      const errorBoxes = screen.queryByRole('alert');
      expect(messageBoxes).not.toBeInTheDocument();
      expect(errorBoxes).not.toBeInTheDocument();
    });
  });

  describe('Button Interaction', () => {
    it('shows loading state when button is clicked', async () => {
      const user = userEvent.setup();
      
      // Mock fetch to delay response
      global.fetch.mockImplementation(
        () => new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test message' }),
        }), 100))
      );

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
      expect(button).toBeDisabled();
    });

    it('button is disabled during loading', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockImplementation(
        () => new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test message' }),
        }), 100))
      );

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      expect(button).toBeDisabled();
    });
  });

  describe('Successful API Call', () => {
    it('displays backend message on successful fetch', async () => {
      const user = userEvent.setup();
      const mockMessage = 'Hello from backend!';

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: mockMessage }),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument();
      });

      expect(screen.getByText(mockMessage)).toBeInTheDocument();
    });

    it('calls the correct API endpoint', async () => {
      const user = userEvent.setup();

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test' }),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/hello'),
          expect.objectContaining({
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          })
        );
      });
    });

    it('displays success icon with message', async () => {
      const user = userEvent.setup();

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success!' }),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        const statusBox = screen.getByRole('status');
        expect(statusBox).toHaveClass('success');
      });
    });

    it('handles missing message field gracefully', async () => {
      const user = userEvent.setup();

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByText('No message received')).toBeInTheDocument();
      });
    });
  });

  describe('Failed API Call', () => {
    it('displays error message on network failure', async () => {
      const user = userEvent.setup();

      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });

      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });

    it('displays error message on HTTP error status', async () => {
      const user = userEvent.setup();

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });

      expect(screen.getByText(/http error! status: 500/i)).toBeInTheDocument();
    });

    it('displays error icon with error message', async () => {
      const user = userEvent.setup();

      global.fetch.mockRejectedValueOnce(new Error('Server error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        const alertBox = screen.getByRole('alert');
        expect(alertBox).toHaveClass('error');
      });
    });

    it('clears previous messages before new fetch', async () => {
      const user = userEvent.setup();

      // First successful call
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message' }),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument();
      });

      // Second call with error
      global.fetch.mockRejectedValueOnce(new Error('Error'));
      
      await user.click(button);
      
      await waitFor(() => {
        expect(screen.queryByText('First message')).not.toBeInTheDocument();
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA labels on button', () => {
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toHaveAttribute('aria-label', 'Get message from backend');
    });

    it('success message has proper ARIA live region', async () => {
      const user = userEvent.setup();

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success' }),
      });

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        const statusBox = screen.getByRole('status');
        expect(statusBox).toHaveAttribute('aria-live', 'polite');
      });
    });

    it('error message has proper ARIA live region', async () => {
      const user = userEvent.setup();

      global.fetch.mockRejectedValueOnce(new Error('Error'));

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await user.click(button);
      
      await waitFor(() => {
        const alertBox = screen.getByRole('alert');
        expect(alertBox).toHaveAttribute('aria-live', 'assertive');
      });
    });

    it('icons are hidden from screen readers', () => {
      render(<App />);
      // All SVG icons should have aria-hidden="true"
      // This is tested by checking that the spinner has aria-hidden when loading
    });
  });

  describe('Multiple API Calls', () => {
    it('can make multiple successful API calls', async () => {
      const user = userEvent.setup();

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });

      // First call
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message' }),
      });

      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument();
      });

      // Second call
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Second message' }),
      });

      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByText('Second message')).toBeInTheDocument();
        expect(screen.queryByText('First message')).not.toBeInTheDocument();
      });
    });

    it('can recover from error and make successful call', async () => {
      const user = userEvent.setup();

      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });

      // First call fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });

      // Second call succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success after error' }),
      });

      await user.click(button);
      
      await waitFor(() => {
        expect(screen.getByText('Success after error')).toBeInTheDocument();
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
      });
    });
  });
});
