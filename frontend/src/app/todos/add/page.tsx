'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createTodo } from '@/services/todoService';
import { TodoCreate } from '@/types/todo';

export default function AddTodoPage() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<number>(3); // Default to medium priority (3)
  const [dueDate, setDueDate] = useState<string>(''); // Store as ISO string
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Prepare todo data
    const todoData: TodoCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      due_date: dueDate || undefined,
    };

    setLoading(true);
    setError(null);

    try {
      const result = await createTodo(todoData);

      if (result.error) {
        setError(result.error);
      } else if (result.data) {
        // Successfully created, navigate back to the todo list
        router.push('/todos');
        router.refresh(); // Refresh to show the new todo
      }
    } catch (err) {
      console.error('Error creating todo:', err);
      setError('An unexpected error occurred while creating the todo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Add New Todo</h1>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={loading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
            placeholder="Enter a title for your todo"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={loading}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
            placeholder="Enter a description (optional)"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="priority"
              value={priority}
              onChange={(e) => setPriority(Number(e.target.value))}
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
            >
              <option value={1}>1 - Highest</option>
              <option value={2}>2 - High</option>
              <option value={3} selected>3 - Medium</option>
              <option value={4}>4 - Low</option>
              <option value={5}>5 - Lowest</option>
            </select>
          </div>

          <div>
            <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-1">
              Due Date
            </label>
            <input
              type="date"
              id="dueDate"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
            />
          </div>
        </div>

        <div className="flex justify-between pt-4">
          <button
            type="button"
            onClick={() => router.back()}
            disabled={loading}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md shadow-sm hover:bg-gray-50 disabled:opacity-50"
          >
            Cancel
          </button>

          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 disabled:opacity-50 flex items-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </>
            ) : 'Add Todo'}
          </button>
        </div>
      </form>
    </div>
  );
}
