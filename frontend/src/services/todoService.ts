import { Todo, TodoCreate, TodoUpdate } from '../types/todo';
import authService from './authService';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Define the shape of our API responses
interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = authService.getToken();
  if (!token) {
    throw new Error('No authentication token found');
  }
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

// Helper function to handle unauthorized responses
const handleUnauthorized = () => {
  // Don't redirect directly from service, just throw an error
  // The calling component will handle the error appropriately
  throw new Error('Authentication required');
};

// Create a new todo
export const createTodo = async (todoData: TodoCreate): Promise<ApiResponse<Todo>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/todos/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(todoData),
    });

    if (response.status === 401) {
      return { error: 'Authentication required' };
    }

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || 'Failed to create todo' };
    }

    const newTodo = await response.json();
    return { data: newTodo };
  } catch (error) {
    console.error('Error creating todo:', error);
    return { error: 'Network error - please try again' };
  }
};

// Get all todos with optional pagination
export const getTodos = async (offset: number = 0, limit: number = 100): Promise<ApiResponse<Todo[]>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/todos/?offset=${offset}&limit=${limit}`, {
      headers: getAuthHeaders(),
    });

    if (response.status === 401) {
      return { error: 'Authentication required' };
    }

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || 'Failed to fetch todos' };
    }

    const todos = await response.json();
    return { data: todos };
  } catch (error) {
    console.error('Error fetching todos:', error);
    return { error: 'Network error - please try again' };
  }
};

// Get a specific todo by ID
export const getTodoById = async (id: number): Promise<ApiResponse<Todo>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      headers: getAuthHeaders(),
    });

    if (response.status === 401) {
      return { error: 'Authentication required' };
    }

    if (!response.ok) {
      const errorData = await response.json();
      if (response.status === 404) {
        return { error: `Todo with ID ${id} not found` };
      }
      return { error: errorData.detail || 'Failed to fetch todo' };
    }

    const todo = await response.json();
    return { data: todo };
  } catch (error) {
    console.error('Error fetching todo:', error);
    return { error: 'Network error - please try again' };
  }
};

// Update a specific todo by ID
export const updateTodo = async (id: number, todoData: TodoUpdate): Promise<ApiResponse<Todo>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(todoData),
    });

    if (response.status === 401) {
      return { error: 'Authentication required' };
    }

    if (!response.ok) {
      const errorData = await response.json();
      if (response.status === 404) {
        return { error: `Todo with ID ${id} not found` };
      }
      return { error: errorData.detail || 'Failed to update todo' };
    }

    const updatedTodo = await response.json();
    return { data: updatedTodo };
  } catch (error) {
    console.error('Error updating todo:', error);
    return { error: 'Network error - please try again' };
  }
};

// Delete a specific todo by ID
export const deleteTodo = async (id: number): Promise<ApiResponse<{ message: string; id: number }>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });

    if (response.status === 401) {
      return { error: 'Authentication required' };
    }

    if (!response.ok) {
      const errorData = await response.json();
      if (response.status === 404) {
        return { error: `Todo with ID ${id} not found` };
      }
      return { error: errorData.detail || 'Failed to delete todo' };
    }

    const result = await response.json();
    return { data: result };
  } catch (error) {
    console.error('Error deleting todo:', error);
    return { error: 'Network error - please try again' };
  }
};