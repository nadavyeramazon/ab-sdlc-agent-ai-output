import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

/**
 * Integration Tests
 * 
 * These tests verify complete user workflows and interactions,
 * simulating real-world usage scenarios.
 */

describe('Integration Tests - User Workflows', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  describe('Complete Success Flow', () => {
    it('should complete full workflow from initial render to success', async () => {
      const user = userEvent.setup();
      const mockMessage = 'Hello from the backend!';
      
      // Mock successful API response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: mockMessage })
      });

      // 1. Initial render
      render(<App />);
      
      // 2. Verify initial state
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument();
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument();
      const backendSaysElements = screen.queryAllByText((content, element) => {
        return element?.classList?.contains('message') && content.includes('Backend says:');
      });
      expect(backendSaysElements).toHaveLength(0);
      
      // 3. User clicks button
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).not.toBeDisabled();
      
      await act(async () => {
        await user.click(button);
      });
      
      // 4. Loading state appears
      await waitFor(() => {
        expect(button).toBeDisabled();
      });
      
      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument();
      });
      
      // 5. Success state appears
      await waitFor(() => {
        const messageDiv = screen.getByText((content, element) => {
          return element?.classList?.contains('message') && content.includes('Backend says:');
        });
        expect(messageDiv).toBeInTheDocument();
        expect(screen.getByText(mockMessage)).toBeInTheDocument();
      });
      
      // 6. Loading state is gone
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      expect(button).not.toBeDisabled();
      
      // 7. No error state
      expect(screen.queryByText(/error:/i)).not.toBeInTheDocument();
    });
  });

  describe('Complete Error Flow', () => {
    it('should complete full workflow from initial render to error', async () => {
      const user = userEvent.setup();
      
      // Mock failed API response
      global.fetch.mockRejectedValueOnce(new Error('Connection refused'));

      // 1. Initial render
      render(<App />);
      
      // 2. Verify initial state
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument();
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).not.toBeDisabled();
      
      // 3. User clicks button
      await act(async () => {
        await user.click(button);
      });
      
      // 4. Loading state appears - button should be disabled
      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument();
      }, { timeout: 3000 });
      
      // 5. Error state appears
      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
        expect(screen.getByText(/connection refused/i)).toBeInTheDocument();
      });
      
      // 6. Loading state is gone and button is re-enabled
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
        expect(button).not.toBeDisabled();
      });
      
      // 7. No success message
      const backendSaysElements = screen.queryAllByText((content, element) => {
        return element?.classList?.contains('message') && content.includes('Backend says:');
      });
      expect(backendSaysElements).toHaveLength(0);
    });
  });

  describe('Error Recovery Flow', () => {
    it('should recover from error and show success on retry', async () => {
      const user = userEvent.setup();
      
      // 1. First attempt fails
      global.fetch.mockRejectedValueOnce(new Error('Network timeout'));
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/network timeout/i)).toBeInTheDocument();
      });
      
      // 2. Second attempt succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success after retry!' })
      });
      
      await act(async () => {
        await user.click(button);
      });
      
      // 3. Verify error is cleared and success is shown
      await waitFor(() => {
        expect(screen.getByText(/success after retry/i)).toBeInTheDocument();
      });
      
      expect(screen.queryByText(/network timeout/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/error:/i)).not.toBeInTheDocument();
    });
  });

  describe('Success Override Flow', () => {
    it('should replace old message with new message', async () => {
      const user = userEvent.setup();
      
      // 1. First successful fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message' })
      });
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument();
      });
      
      // 2. Second successful fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Second message' })
      });
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/second message/i)).toBeInTheDocument();
      });
      
      // 3. First message should be gone
      expect(screen.queryByText(/first message/i)).not.toBeInTheDocument();
    });
  });

  describe('Success to Error Flow', () => {
    it('should transition from success to error state', async () => {
      const user = userEvent.setup();
      
      // 1. First attempt succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Initial success' })
      });
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/initial success/i)).toBeInTheDocument();
      });
      
      // 2. Second attempt fails
      global.fetch.mockRejectedValueOnce(new Error('Backend unavailable'));
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/backend unavailable/i)).toBeInTheDocument();
      });
      
      // 3. Success message should be gone
      expect(screen.queryByText(/initial success/i)).not.toBeInTheDocument();
      const backendSaysElements = screen.queryAllByText((content, element) => {
        return element?.classList?.contains('message') && content.includes('Backend says:');
      });
      expect(backendSaysElements).toHaveLength(0);
    });
  });

  describe('Multiple Sequential Requests', () => {
    it('should handle three consecutive successful requests', async () => {
      const user = userEvent.setup();
      const messages = ['Message 1', 'Message 2', 'Message 3'];
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      for (let i = 0; i < messages.length; i++) {
        global.fetch.mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: messages[i] })
        });
        
        await act(async () => {
          await user.click(button);
        });
        
        await waitFor(() => {
          expect(screen.getByText(messages[i])).toBeInTheDocument();
        });
        
        // Previous messages should not be visible
        for (let j = 0; j < i; j++) {
          expect(screen.queryByText(messages[j])).not.toBeInTheDocument();
        }
      }
      
      // Verify fetch was called correct number of times
      expect(global.fetch).toHaveBeenCalledTimes(3);
    });
  });

  describe('Alternating Success and Error Flow', () => {
    it('should handle alternating success and error states', async () => {
      const user = userEvent.setup();
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // 1. Success
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success 1' })
      });
      await act(async () => {
        await user.click(button);
      });
      await waitFor(() => {
        expect(screen.getByText(/success 1/i)).toBeInTheDocument();
      });
      
      // 2. Error
      global.fetch.mockRejectedValueOnce(new Error('Error 1'));
      await act(async () => {
        await user.click(button);
      });
      await waitFor(() => {
        expect(screen.getByText(/error 1/i)).toBeInTheDocument();
      });
      expect(screen.queryByText(/success 1/i)).not.toBeInTheDocument();
      
      // 3. Success again
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Success 2' })
      });
      await act(async () => {
        await user.click(button);
      });
      await waitFor(() => {
        expect(screen.getByText(/success 2/i)).toBeInTheDocument();
      });
      expect(screen.queryByText(/error 1/i)).not.toBeInTheDocument();
      
      // 4. Error again
      global.fetch.mockRejectedValueOnce(new Error('Error 2'));
      await act(async () => {
        await user.click(button);
      });
      await waitFor(() => {
        expect(screen.getByText(/error 2/i)).toBeInTheDocument();
      });
      expect(screen.queryByText(/success 2/i)).not.toBeInTheDocument();
    });
  });

  describe('User Experience Flow', () => {
    it('should provide clear feedback throughout the user journey', async () => {
      const user = userEvent.setup();
      
      render(<App />);
      
      // 1. User sees welcoming interface
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument();
      const button = screen.getByRole('button', { name: /get message from backend/i });
      expect(button).toBeEnabled();
      
      // 2. User initiates action
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      global.fetch.mockReturnValueOnce(promise);
      
      await act(async () => {
        await user.click(button);
      });
      
      // 3. Immediate feedback: button disabled and loading
      await waitFor(() => {
        expect(button).toBeDisabled();
        expect(screen.getByText(/loading/i)).toBeInTheDocument();
      });
      
      // 4. Action completes with success
      await act(async () => {
        resolvePromise({
          ok: true,
          json: async () => ({ message: 'Backend response!' })
        });
      });
      
      await waitFor(() => {
        expect(screen.getByText(/backend response!/i)).toBeInTheDocument();
      });
      
      // 5. User can interact again
      expect(button).toBeEnabled();
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });
  });

  describe('API Contract Verification', () => {
    it('should call correct API endpoint with no parameters', async () => {
      const user = userEvent.setup();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test' })
      });
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await act(async () => {
        await user.click(button);
      });
      
      // Verify API call
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello');
        expect(global.fetch).toHaveBeenCalledTimes(1);
      });
    });

    it('should handle API response structure correctly', async () => {
      const user = userEvent.setup();
      
      const mockResponse = {
        message: 'Test message with special chars: !@#$%^&*()'
      };
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });
      
      render(<App />);
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(mockResponse.message)).toBeInTheDocument();
      });
    });
  });

  describe('State Persistence During Operations', () => {
    it('should maintain heading visibility through all state changes', async () => {
      const user = userEvent.setup();
      
      render(<App />);
      const heading = screen.getByRole('heading', { name: /hello world/i });
      const button = screen.getByRole('button', { name: /get message from backend/i });
      
      // Heading visible initially
      expect(heading).toBeInTheDocument();
      
      // Heading visible during loading
      let resolvePromise;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      global.fetch.mockReturnValueOnce(promise);
      
      await act(async () => {
        await user.click(button);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument();
      });
      expect(heading).toBeInTheDocument();
      
      // Heading visible after success
      await act(async () => {
        resolvePromise({
          ok: true,
          json: async () => ({ message: 'Test' })
        });
      });
      
      await waitFor(() => {
        expect(screen.getByText(/test/i)).toBeInTheDocument();
      });
      expect(heading).toBeInTheDocument();
      
      // Heading visible after error
      global.fetch.mockRejectedValueOnce(new Error('Error'));
      await act(async () => {
        await user.click(button);
      });
      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument();
      });
      expect(heading).toBeInTheDocument();
    });
  });
});
