from .engine import TodoManager

def main():
    """Main function to run the CLI to-do application."""
    manager = TodoManager()
    print("Welcome to the To-Do CLI!")

    while True:
        command = input("> ").strip().lower()
        parts = command.split(" ", 1)
        action = parts[0]

        match action:
            case "add":
                if len(parts) > 1:
                    task = manager.add_task(parts[1])
                    print(f"Added task {task.id}: '{task.title}'")
                else:
                    print("Usage: add <task title>")
            case "view":
                tasks = manager.list_tasks()
                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        status = "✓" if task.is_completed else " "
                        print(f"[{status}] {task.id}: {task.title}")
            case "done":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    task = manager.mark_complete(task_id)
                    if task:
                        print(f"Completed task {task.id}: '{task.title}'")
                    else:
                        print(f"Task with ID {task_id} not found.")
                else:
                    print("Usage: done <task id>")
            case "del":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if manager.delete_task(task_id):
                        print(f"Deleted task {task_id}.")
                    else:
                        print(f"Task with ID {task_id} not found.")
                else:
                    print("Usage: del <task id>")
            case "exit":
                print("Goodbye!")
                break
            case "help":
                print("\nAvailable commands:")
                print("  add <task title> - Add a new task")
                print("  view               - View all tasks")
                print("  done <task id>     - Mark a task as complete")
                print("  del <task id>      - Delete a task")
                print("  exit               - Exit the application\n")
            case _:
                print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
