import React from 'react';
import ChatWindow from '../components/ChatInterface/ChatWindow';
import { useAuth } from '../contexts/AuthContext';

const ChatPage: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6 text-center">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-6">
            You need to be logged in to access the AI chat assistant.
          </p>
          <a
            href="/login"
            className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
          >
            Log In
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-2">AI Todo Assistant</h1>
            <p className="text-gray-600 mb-6">
              Manage your tasks with natural language. Create, update, and organize your todos using simple commands.
            </p>

            <div className="h-[500px]">
              <ChatWindow userId={user.id} />
            </div>
          </div>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Try commands like: "Create a new task to buy groceries", "Show me my tasks for today", or "Mark grocery shopping as complete"</p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;