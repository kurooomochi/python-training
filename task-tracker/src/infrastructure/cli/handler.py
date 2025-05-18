import argparse
from src.application.TodoService_adapter import TodoService
from src.domain.Task import TaskStatusEnum


class CLIHandler:
    """
    Handles command-line interface interactions for the Task Tracker application.

    It uses argparse to define and parse command-line arguments and then
    delegates the operations to the TodoService.
    """
    def __init__(self, service: TodoService):
        """
        Initializes the CLIHandler with a TodoService instance.

        Args:
            service (TodoService): The service layer to interact with.
        """
        self._service = service
        self.parser = self._setup_parser()
    
    def _setup_parser(self) -> argparse.ArgumentParser:
        """
        Sets up the argparse.ArgumentParser with all the available commands and arguments.

        Returns:
            argparse.ArgumentParser: The configured argument parser.
        """
        parser = argparse.ArgumentParser(
            prog="task-tracker",
            description="A simple command-line task tracker application.",
            epilog="Example: python main.py add \"Buy milk\""
        )
        subparsers = parser.add_subparsers(
            title="Commands", 
            dest="command", 
            required=True, 
            help="Available actions"
        )
        
        # Add command: Adds a new task
        parser_add = subparsers.add_parser("add", help="Add a new task to the list.")
        parser_add.add_argument("description", type=str, help="The description of the task.")
    
        # List command: Lists all tasks, optionally filtered by status
        parser_list = subparsers.add_parser("list", help="List all tasks or filter by status.")
        parser_list.add_argument(
            "--status", 
            type=str, 
            choices=[status.value for status in TaskStatusEnum], 
            help="Filter tasks by status (e.g., 'to do', 'in progress', 'done').", 
            required=False, 
            default=None
        )
        
        # Get command: Retrieves a specific task by its ID
        parser_get = subparsers.add_parser("get", help="Get a specific task by its ID.")
        parser_get.add_argument("id", type=int, help="The ID of the task to retrieve.")
        
        # Remove command: Deletes a task by its ID
        parser_remove = subparsers.add_parser("remove", help="Remove a task by its ID.")
        parser_remove.add_argument("id", type=int, help="The ID of the task to remove.")
        
        # Mark-done command: Marks a task as done
        parser_done = subparsers.add_parser("mark-done", help="Mark a task as 'done'.")
        parser_done.add_argument("id", type=int, help="The ID of the task to mark as done.")
        
        # Mark-in-progress command: Marks a task as in progress
        parser_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as 'in progress'.")
        parser_in_progress.add_argument("id", type=int, help="The ID of the task to mark as in progress.")

        # Mark-todo command: Marks a task as to do
        parser_todo = subparsers.add_parser("mark-todo", help="Mark a task as 'to do'.")
        parser_todo.add_argument("id", type=int, help="The ID of the task to mark as to do.")
        
        return parser
    
    def handle(self, args=None):
        """
        Parses the command-line arguments and executes the corresponding action.

        Args:
            args (Optional[List[str]]): A list of command-line arguments. 
                                         If None, sys.argv[1:] is used.
        """
        parsed_args = self.parser.parse_args(args)
        
        try:
            if parsed_args.command == "add":
                task = self._service.add_task(parsed_args.description)
                print(f"Task Added: {task}")
            elif parsed_args.command == "list":
                # Convert string status to TaskStatusEnum if provided
                status_enum = TaskStatusEnum(parsed_args.status) if parsed_args.status else None
                tasks = self._service.list_tasks(status=status_enum)
                if not tasks:
                    status_message = f' with status "{parsed_args.status}"' if parsed_args.status else ""
                    print(f"No tasks found{status_message}.")
                else:
                    print("To-Do List:")
                    for task_item in tasks:
                        print(f"- {task_item}")
            elif parsed_args.command == "get":
                task = self._service.get_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    print(f"Task details: {task}")
            elif parsed_args.command == "remove":
                success = self._service.remove_task(parsed_args.id)
                if not success:
                    print(f"Error: Task with ID {parsed_args.id} not found or could not be removed.")
                else:
                    print(f"Task with ID {parsed_args.id} removed successfully.")
            elif parsed_args.command == "mark-done":
                task = self._service.complete_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    print(f"Task marked as done: {task}")
            elif parsed_args.command == "mark-in-progress":
                task = self._service.begin_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    print(f"Task marked as in progress: {task}")
            elif parsed_args.command == "mark-todo":
                task = self._service.get_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    task.mark_as_todo()
                    updated_task = self._service.repository.update(task)
                    if updated_task:
                        print(f"Task marked as to-do: {updated_task}")
                    else:
                        print(f"Error: Could not update task with ID {parsed_args.id}.")

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please check your command and try again.")