'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleRedirect = () => {
    setIsLoading(true);
    // The redirect will happen via the Link component
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Navigation */}
      <nav className="bg-white shadow-sm py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="text-xl font-bold text-indigo-600">Todo App</div>
            <div className="flex space-x-4">
              <Link
                href="/todos"
                className="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Todos
              </Link>
              <Link
                href="/todos/add"
                className="bg-indigo-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors"
              >
                Add Todo
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center p-4">
        <div className="max-w-3xl w-full bg-white rounded-xl shadow-lg p-8 space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
              Welcome to Your Todo App
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              A full-stack application for managing your daily tasks efficiently.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
              <h3 className="font-semibold text-blue-800 mb-2">Add Tasks</h3>
              <p className="text-gray-600 text-sm">
                Create new todos with titles, descriptions, priorities, and due dates.
              </p>
            </div>
            <div className="bg-green-50 p-6 rounded-lg border border-green-100">
              <h3 className="font-semibold text-green-800 mb-2">Organize</h3>
              <p className="text-gray-600 text-sm">
                Manage your tasks with priority levels and due dates.
              </p>
            </div>
            <div className="bg-purple-50 p-6 rounded-lg border border-purple-100">
              <h3 className="font-semibold text-purple-800 mb-2">Track</h3>
              <p className="text-gray-600 text-sm">
                Monitor your progress and mark tasks as complete.
              </p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/todos"
              onClick={handleRedirect}
              className={`px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg shadow-md hover:bg-indigo-700 transition-colors flex items-center justify-center ${
                isLoading ? 'opacity-75 cursor-not-allowed' : ''
              }`}
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading Todos...
                </>
              ) : 'View My Todos'}
            </Link>

            <Link
              href="/todos/add"
              className="px-6 py-3 bg-white text-indigo-600 font-medium rounded-lg border border-indigo-300 shadow-sm hover:bg-indigo-50 transition-colors flex items-center justify-center"
            >
              Add New Todo
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} Todo App. Built with Next.js and FastAPI.
          </p>
        </div>
      </footer>
    </div>
  );
}