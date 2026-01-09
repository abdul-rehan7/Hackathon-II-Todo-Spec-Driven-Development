'use client';

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UpdateTodoPage from '../../src/app/todos/[id]/edit/page';
import '@testing-library/jest-dom';
import { usePathname } from 'next/navigation';

// Mock Next.js useRouter and usePathname
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(() => ({
    push: mockPush,
  })),
  usePathname: jest.fn(),
}));

const mockTodo = {
  id: 1,
  title: 'Existing Todo',
  completed: false,
  priority: 'Medium',
  tags: ['work', 'urgent'],
  due_date: '2026-02-15',
};

const mockFetch = jest.fn((url: string) => {
  if (url === '/api/v1/todos/1') {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockTodo),
    });
  }
  return Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ ...mockTodo, title: 'Updated Todo' }),
  });
});

global.fetch = mockFetch as any;

describe('UpdateTodoPage', () => {
  beforeEach(() => {
    mockPush.mockClear();
    mockFetch.mockClear();
    (usePathname as jest.Mock).mockReturnValue('/todos/1/edit');
  });

  it('renders loading state initially', () => {
    mockFetch.mockReturnValueOnce(new Promise(() => {})); // Never resolve to keep loading
    render(<UpdateTodoPage params={{ id: '1' }} />);
    expect(screen.getByText('Loading todo...')).toBeInTheDocument();
  });

  it('renders error state if fetch fails', async () => {
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        statusText: 'Not Found',
      })
    );
    render(<UpdateTodoPage params={{ id: '1' }} />);
    await waitFor(() => {
      expect(screen.getByText(/Error: Not Found/i)).toBeInTheDocument();
    });
  });

  it('pre-fills the form with existing todo data', async () => {
    render(<UpdateTodoPage params={{ id: '1' }} />);
    await waitFor(() => {
      expect(screen.getByLabelText(/Title/i)).toHaveValue(mockTodo.title);
      expect(screen.getByLabelText(/Completed/i)).not.toBeChecked();
      expect(screen.getByLabelText(/Priority/i)).toHaveValue(mockTodo.priority);
      expect(screen.getByLabelText(/Tags \(comma-separated\)/i)).toHaveValue(mockTodo.tags.join(', '));
      expect(screen.getByLabelText(/Due Date/i)).toHaveValue(mockTodo.due_date);
    });
  });

  it('updates todo details on form submission and redirects', async () => {
    render(<UpdateTodoPage params={{ id: '1' }} />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Title/i)).toHaveValue(mockTodo.title);
    });

    const titleInput = screen.getByLabelText(/Title/i);
    const completedCheckbox = screen.getByLabelText(/Completed/i);
    const prioritySelect = screen.getByLabelText(/Priority/i);
    const tagsInput = screen.getByLabelText(/Tags \(comma-separated\)/i);
    const dueDateInput = screen.getByLabelText(/Due Date/i);
    const submitButton = screen.getByRole('button', { name: /Update Todo/i });

    fireEvent.change(titleInput, { target: { value: 'New Title' } });
    fireEvent.click(completedCheckbox);
    fireEvent.change(prioritySelect, { target: { value: 'High' } });
    fireEvent.change(tagsInput, { target: { value: 'dev, review' } });
    fireEvent.change(dueDateInput, { target: { value: '2026-03-01' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(2); // One for GET, one for PUT
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/v1/todos/1',
        expect.objectContaining({
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: 'New Title',
            completed: true,
            priority: 'High',
            tags: ['dev', 'review'],
            due_date: '2026-03-01',
          }),
        })
      );
      expect(mockPush).toHaveBeenCalledWith('/todos');
    });
  });

  it('handles API error gracefully on update', async () => {
    mockFetch.mockImplementationOnce((url: string) => {
      if (url === '/api/v1/todos/1') {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockTodo),
        });
      }
      return Promise.resolve({
        ok: false,
        statusText: 'Internal Server Error',
      });
    });

    render(<UpdateTodoPage params={{ id: '1' }} />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Title/i)).toHaveValue(mockTodo.title);
    });

    const submitButton = screen.getByRole('button', { name: /Update Todo/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(2); // One for GET, one for PUT
      // Expect an error to be logged or displayed, but no redirection
      expect(mockPush).not.toHaveBeenCalled();
    });
  });
});
