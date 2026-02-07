import React from 'react';
import { ChatMessage } from '../../types/chat';
import MessageBubble from './MessageBubble';

interface ChatHistoryProps {
  messages: ChatMessage[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  if (!messages || messages.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        No chat history available. Start a conversation with the AI assistant!
      </div>
    );
  }

  return (
    <div className="overflow-y-auto">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  );
};

export default ChatHistory;