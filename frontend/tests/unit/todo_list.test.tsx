import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import TodoListPage from '../../src/app/todos/page';
import '@testing-library/jest-dom';

// Mock Next.js Link
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  );
});

// Mock global fetch
const mockTodos = [
  { id: 1, title: 'Todo 1', completed: false, priority: 'Medium', tags: ['work'], due_date: '2026-01-31' },
  { id: 2, title: 'Todo 2', completed: true, priority: 'Low', tags: ['personal'], due_date: null },
];

const mockFetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve(mockTodos),
  })
);

global.fetch = mockFetch as any;

describe('TodoListPage', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders loading state initially', () => {
    mockFetch.mockReturnValueOnce(new Promise(() => {})); // Never resolve to keep loading
    render(<TodoListPage />);
    expect(screen.getByText('Loading todos...')).toBeInTheDocument();
  });

  it('renders error state if fetch fails', async () => {
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        statusText: 'Network Error',
      })
    );
    render(<TodoListPage />);
    await waitFor(() => {
      expect(screen.getByText(/Error: Network Error/i)).toBeInTheDocument();
    });
  });

  it('renders todos fetched from the API', async () => {
    render(<TodoListPage />);
    await waitFor(() => {
      expect(screen.getByText('Todo List')).toBeInTheDocument();
      expect(screen.getByText('Add New Todo')).toBeInTheDocument();
      expect(screen.getByText('Todo 1')).toBeInTheDocument();
      expect(screen.getByText('Priority: Medium')).toBeInTheDocument();
      expect(screen.getByText('Tags: work')).toBeInTheDocument();
      expect(screen.getByText('Due: 2026-01-31')).toBeInTheDocument();
      expect(screen.getByText('Todo 2')).toBeInTheDocument();
      expect(screen.getByText('Priority: Low')).toBeInTheDocument();
      expect(screen.getByText('Tags: personal')).toBeInTheDocument();
      expect(screen.queryByText('Due: ')).not.toBeInTheDocument(); // Todo 2 has no due date

      const todo1 = screen.getByText('Todo 1');
      expect(todo1).not.toHaveClass('line-through');

      const todo2 = screen.getByText('Todo 2');
      expect(todo2).toHaveClass('line-through');
    });
  });

  it('renders "No todos found" message if API returns empty array', async () => {
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );
    render(<TodoListPage />);
    await waitFor(() => {
      expect(screen.getByText('No todos found. Add a new one!')).toBeInTheDocument();
    });
  });

  it('deletes a todo item when the delete button is clicked', async () => {
    const initialTodos = [
      { id: 1, title: 'Todo to Delete', completed: false, priority: 'Medium', tags: ['test'], due_date: null },
      { id: 2, title: 'Another Todo', completed: false, priority: 'Low', tags: [], due_date: null },
    ];

    // Mock fetch for initial render (GET all todos)
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(initialTodos),
      })
    );

    // Mock fetch for delete request (DELETE a todo)
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: 'Todo deleted successfully' }),
      })
    );

    // Mock window.confirm
    jest.spyOn(window, 'confirm').mockReturnValue(true);

    render(<TodoListPage />);

    await waitFor(() => {
      expect(screen.getByText('Todo to Delete')).toBeInTheDocument();
      expect(screen.getByText('Another Todo')).toBeInTheDocument();
    });

    const deleteButton = screen.getAllByRole('button', { name: /Delete/i })[0];
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this todo?');
      expect(mockFetch).toHaveBeenCalledTimes(2); // One for GET, one for DELETE
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/v1/todos/1',
        expect.objectContaining({
          method: 'DELETE',
        })
      );
      expect(screen.queryByText('Todo to Delete')).not.toBeInTheDocument();
      expect(screen.getByText('Another Todo')).toBeInTheDocument();
    });
  });
});
