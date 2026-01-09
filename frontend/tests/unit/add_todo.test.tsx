import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AddTodo from '../../src/components/AddTodo'; // Assuming the component will be here
import { createTodo } from '../../src/services/todoService'; // Mock this service

// Mock the todo service
jest.mock('../../src/services/todoService', () => ({
  createTodo: jest.fn(),
}));

describe('AddTodo', () => {
  beforeEach(() => {
    // Reset mock before each test
    (createTodo as jest.Mock).mockClear();
  });

  test('renders the AddTodo form', () => {
    render(<AddTodo />);
    expect(screen.getByLabelText(/Title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Priority/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Due Date/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Add Todo/i })).toBeInTheDocument();
  });

  test('allows entering a title and description', () => {
    render(<AddTodo />);
    const titleInput = screen.getByLabelText(/Title/i);
    const descriptionInput = screen.getByLabelText(/Description/i);

    fireEvent.change(titleInput, { target: { value: 'New Test Todo' } });
    fireEvent.change(descriptionInput, { target: { value: 'This is a test description.' } });

    expect(titleInput).toHaveValue('New Test Todo');
    expect(descriptionInput).toHaveValue('This is a test description.');
  });

  test('calls createTodo and clears form on successful submission', async () => {
    (createTodo as jest.Mock).mockResolvedValue({ id: 1, title: 'New Test Todo', completed: false });

    render(<AddTodo />);
    const titleInput = screen.getByLabelText(/Title/i);
    const addButton = screen.getByRole('button', { name: /Add Todo/i });

    fireEvent.change(titleInput, { target: { value: 'New Test Todo' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(createTodo).toHaveBeenCalledTimes(1);
      expect(createTodo).toHaveBeenCalledWith({
        title: 'New Test Todo',
        description: '',
        priority: 1, // Default priority
        due_date: null,
      });
      expect(titleInput).toHaveValue(''); // Form should clear after submission
    });
  });

  test('shows an error message on failed submission', async () => {
    (createTodo as jest.Mock).mockRejectedValue(new Error('Failed to create todo'));

    render(<AddTodo />);
    const titleInput = screen.getByLabelText(/Title/i);
    const addButton = screen.getByRole('button', { name: /Add Todo/i });

    fireEvent.change(titleInput, { target: { value: 'Failing Todo' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByText(/Failed to create todo/i)).toBeInTheDocument();
    });
  });
});
