'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getTodos, deleteTodo } from '@/services/todoService';
import { Todo } from '@/types/todo';

export default function TodoListPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this todo? This action cannot be undone.')) {
      return;
    }

    try {
      const result = await deleteTodo(id);

      if (result.error) {
        setError(result.error);
      } else {
        // Remove the deleted todo from the local state
        setTodos(todos.filter(todo => todo.id !== id));
      }
    } catch (err) {
      console.error('Error deleting todo:', err);
      setError('An unexpected error occurred while deleting the todo.');
    }
  };

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const result = await getTodos();

        if (result.error) {
          setError(result.error);
        } else if (result.data) {
          setTodos(result.data);
        }
      } catch (err) {
        console.error('Error fetching todos:', err);
        setError('An unexpected error occurred while fetching todos.');
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, []);

  // Function to get priority label for display
  const getPriorityLabel = (priority: number): string => {
    switch (priority) {
      case 1: return '1 - Highest';
      case 2: return '2 - High';
      case 3: return '3 - Medium';
      case 4: return '4 - Low';
      case 5: return '5 - Lowest';
      default: return `${priority} - Unknown`;
    }
  };

  // Function to format date for display
  const formatDate = (dateString: string | undefined | null): string => {
    if (!dateString) return '';

    try {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4 max-w-4xl">
        <h1 className="text-2xl font-bold mb-6">Todo List</h1>
        <div className="flex justify-center items-center py-12">
          <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="ml-2">Loading todos...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4 max-w-4xl">
        <h1 className="text-2xl font-bold mb-6">Todo List</h1>
        <div className="p-4 bg-red-100 text-red-700 rounded-md">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Todo List</h1>
        <Link
          href="/todos/add"
          className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 transition-colors"
        >
          Add New Todo
        </Link>
      </div>

      {todos.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No todos found. Add a new one to get started!</p>
          <Link
            href="/todos/add"
            className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 transition-colors"
          >
            Create Your First Todo
          </Link>
        </div>
      ) : (
        <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                  Title
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Status
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Priority
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Due Date
                </th>
                <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {todos.map((todo) => (
                <tr key={todo.id} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                    <span className={`${todo.completed ? 'line-through text-gray-500' : ''}`}>
                      {todo.title}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                      todo.completed
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {todo.completed ? 'Completed' : 'Pending'}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                      todo.priority <= 2
                        ? 'bg-red-100 text-red-800'
                        : todo.priority <= 3
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-blue-100 text-blue-800'
                    }`}>
                      {getPriorityLabel(todo.priority)}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {formatDate(todo.due_date as string)}
                  </td>
                  <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <div className="flex justify-end space-x-2">
                      <Link
                        href={`/todos/${todo.id}/edit`}
                        className="text-indigo-600 hover:text-indigo-900 px-3 py-1 rounded hover:bg-indigo-50"
                      >
                        Edit
                      </Link>
                      <button
                        className="text-red-600 hover:text-red-900 px-3 py-1 rounded hover:bg-red-50"
                        onClick={() => handleDelete(todo.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
