import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage } from '../../types/chat';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import { sendChatMessage } from '../../services/todoService';

interface ChatWindowProps {
  userId?: string;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ userId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Sample initial messages
  useEffect(() => {
    setMessages([
      {
        id: '1',
        message: 'Hello! I\'m your AI assistant. You can create, update, or manage your todos using natural language. Try saying "Create a new task to buy groceries"',
        sender: 'system',
        timestamp: new Date(Date.now() - 30000)
      }
    ]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (messageText: string) => {
    if (!userId) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          message: messageText,
          sender: 'user',
          timestamp: new Date()
        },
        {
          id: (Date.now() + 1).toString(),
          message: 'Please log in to use the chat functionality.',
          sender: 'system',
          timestamp: new Date()
        }
      ]);
      return;
    }

    // Check if the message contains destructive actions (delete, complete)
    const lowerMsg = messageText.toLowerCase();
    const isDestructiveAction = /delete|remove|cancel|finish|done|complete|mark as done|eliminate|get rid of|scrub|erase|wipe|clear|discard|throw away|trash|dispose of|cross off|check off/.test(lowerMsg);

    // If it's a destructive action, show a confirmation dialog
    if (isDestructiveAction) {
      const confirmed = window.confirm(`You're about to perform a destructive action: "${messageText}". Are you sure you want to proceed?`);
      if (!confirmed) {
        // Add a message to indicate the action was cancelled
        const cancellationMessage: ChatMessage = {
          id: Date.now().toString(),
          message: `Action cancelled: "${messageText}"`,
          sender: 'system',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, cancellationMessage]);
        return;
      }
    }

    // Add user message to the chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      message: messageText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call the API to get AI response
      const response = await sendChatMessage(messageText);

      if (response.data) {
        const aiMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          message: response.data.response,
          sender: 'system',
          timestamp: new Date(),
          intent: response.data.intent,
          actionTaken: response.data.action_taken
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          message: response.error || 'Sorry, I encountered an error processing your request.',
          sender: 'system',
          timestamp: new Date()
        };

        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        message: 'Sorry, I encountered an error connecting to the AI service.',
        sender: 'system',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md overflow-hidden">
      <div className="bg-blue-500 text-white p-4">
        <h2 className="text-xl font-bold">AI Todo Assistant</h2>
        <p className="text-sm opacity-80">Manage your tasks with natural language</p>
      </div>

      <div className="flex-grow overflow-y-auto p-4 bg-gray-50" style={{ maxHeight: '400px' }}>
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-gray-200 bg-white">
        <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatWindow;