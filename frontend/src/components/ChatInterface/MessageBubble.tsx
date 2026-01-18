import React from 'react';
import { ChatMessage } from '../../types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-xs md:max-w-md px-4 py-2 rounded-lg ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        <p className="whitespace-pre-wrap">{message.message}</p>

        {/* Display action taken data for system messages */}
        {!isUser && message.actionTaken && Object.keys(message.actionTaken).length > 0 && (
          <div className="mt-2 text-xs bg-gray-300 bg-opacity-50 p-2 rounded">
            <details className="cursor-pointer">
              <summary className="font-medium">Details</summary>
              <pre className="text-xs mt-1 overflow-x-auto">
                {JSON.stringify(message.actionTaken, null, 2)}
              </pre>
            </details>
          </div>
        )}

        <div className={`text-xs mt-1 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;