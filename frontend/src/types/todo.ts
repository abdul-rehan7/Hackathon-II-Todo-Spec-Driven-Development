// Define the Todo type that matches the backend model
export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: number; // 1 (high) to 5 (low)
  due_date?: Date | string | null; // Can be Date object or ISO string from API
}

// Define the type for creating a new todo
export interface TodoCreate {
  title: string;
  description?: string;
  priority?: number; // 1 (high) to 5 (low), defaults to 1
  due_date?: Date | string; // Can be Date object or ISO string
}

// Define the type for updating a todo
export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: number; // 1 (high) to 5 (low)
  due_date?: Date | string | null; // Can be Date object or ISO string, or null to clear
}