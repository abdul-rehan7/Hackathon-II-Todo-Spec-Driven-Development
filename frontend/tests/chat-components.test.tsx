import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MessageBubble from '../src/components/ChatInterface/MessageBubble';
import InputArea from '../src/components/ChatInterface/InputArea';
import ChatWindow from '../src/components/ChatInterface/ChatWindow';
import { ChatMessage } from '../src/types/chat';

// Mock the sendChatMessage function
jest.mock('../src/services/todoService', () => ({
  sendChatMessage: jest.fn()
}));

describe('Chat UI Components', () => {
  describe('MessageBubble', () => {
    const mockMessage: ChatMessage = {
      id: '1',
      message: 'Hello, world!',
      sender: 'user',
      timestamp: new Date()
    };

    test('renders user message correctly', () => {
      render(<MessageBubble message={mockMessage} />);

      expect(screen.getByText('Hello, world!')).toBeInTheDocument();
      expect(screen.getByText('Hello, world!')).toHaveClass('bg-blue-500'); // User messages have blue background
    });

    test('renders system message correctly', () => {
      const systemMessage: ChatMessage = {
        ...mockMessage,
        sender: 'system',
        message: 'System message'
      };

      render(<MessageBubble message={systemMessage} />);

      expect(screen.getByText('System message')).toBeInTheDocument();
      expect(screen.getByText('System message')).toHaveClass('bg-gray-200'); // System messages have gray background
    });

    test('displays timestamp', () => {
      render(<MessageBubble message={mockMessage} />);

      // Check that a time is displayed
      const timeElement = screen.getByText(/am|pm/i); // Look for AM/PM indicator
      expect(timeElement).toBeInTheDocument();
    });

    test('shows action taken details for system messages', () => {
      const messageWithAction: ChatMessage = {
        ...mockMessage,
        sender: 'system',
        message: 'Todo created successfully',
        actionTaken: { todo_id: 1, content: 'Buy groceries' }
      };

      render(<MessageBubble message={messageWithAction} />);

      const detailsSummary = screen.getByText('Details');
      expect(detailsSummary).toBeInTheDocument();
    });
  });

  describe('InputArea', () => {
    test('renders input field and send button', () => {
      render(<InputArea onSendMessage={jest.fn()} isLoading={false} />);

      expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
    });

    test('displays loading state', () => {
      render(<InputArea onSendMessage={jest.fn()} isLoading={true} />);

      const sendButton = screen.getByRole('button');
      expect(sendButton).toBeDisabled();
      expect(sendButton).toHaveTextContent('Sending...');
    });

    test('disables send button when input is empty', () => {
      render(<InputArea onSendMessage={jest.fn()} isLoading={false} />);

      const input = screen.getByPlaceholderText('Type your message here...');
      const sendButton = screen.getByRole('button', { name: 'Send' });

      expect(sendButton).toBeDisabled();

      fireEvent.change(input, { target: { value: 'Test message' } });
      expect(sendButton).not.toBeDisabled();
    });

    test('calls onSendMessage when form is submitted', () => {
      const mockOnSendMessage = jest.fn();
      render(<InputArea onSendMessage={mockOnSendMessage} isLoading={false} />);

      const input = screen.getByPlaceholderText('Type your message here...');
      const form = screen.getByRole('form');

      fireEvent.change(input, { target: { value: 'Test message' } });
      fireEvent.submit(form);

      expect(mockOnSendMessage).toHaveBeenCalledWith('Test message');
      expect(input).toHaveValue(''); // Input should be cleared after submission
    });
  });

  describe('ChatWindow', () => {
    test('renders chat interface elements', () => {
      render(<ChatWindow userId="test-user-id" />);

      expect(screen.getByText('AI Todo Assistant')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
    });

    test('shows welcome message initially', async () => {
      render(<ChatWindow userId="test-user-id" />);

      // Wait for the initial message to appear
      await waitFor(() => {
        expect(screen.getByText(/Hello! I'm your AI assistant/i)).toBeInTheDocument();
      });
    });

    test('handles user without userId properly', () => {
      render(<ChatWindow userId={undefined} />);

      // Should show login prompt or error message when no user ID
      expect(screen.getByText('Please log in to use the chat functionality.')).toBeInTheDocument();
    });
  });
});