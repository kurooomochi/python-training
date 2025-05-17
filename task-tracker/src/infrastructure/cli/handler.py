import argparse
from application.TodoService_adapter import TodoService
from domain.Task import TaskStatusEnum


class CLIHandler:
    def __init__(self, service: TodoService):
        self._service = service
        self.parser = self._setup_parser()
    
    def _setup_parser(self):
        parser = argparse.ArgumentParser(
            prog="task-tracker",
            description="Task Tracker application",
        )
        subparsers = parser.add_subparsers(
            title="Commands", 
            dest="command", 
            required=True, 
            help="Available Commands"
        )
        
        # Add command
        parser_add = subparsers.add_parser("add", help="Add a new task.")
        parser_add.add_argument("description", type=str, help="The description of the task.")
    
        # List command
        parser_list = subparsers.add_parser("list", help="List all tasks.")
        parser_list.add_argument("--status", type=TaskStatusEnum, help="The status of the tasks to retrieve (optional)", required=False, default=None) # Changed "status" to "--status" and added default
        
        # Get Task by ID
        parser_get = subparsers.add_parser("get", help="Get task by ID.")
        parser_get.add_argument("id", type=int, help="The ID of the task to retrieve.")
        
        # Remove task
        parser_remove = subparsers.add_parser("remove", help="Remove a task.")
        parser_remove.add_argument("id", type=int, help="The ID of the task to remove.")
        
        # Mark task as done
        parser_done = subparsers.add_parser("mark-done", help="Mark a task as done.")
        parser_done.add_argument("id", type=int, help="The ID of the task to complete.")
        
        # Mark task as in progress
        parser_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as in progress.")
        parser_in_progress.add_argument("id", type=int, help="The ID of the task to complete.")
        
        return parser
    
    def handle(self, args=None):
        parsed_args = self.parser.parse_args(args)
        try:
            if parsed_args.command == "add":
                task = self._service.add_task(parsed_args.description)
                print(f"Task Added: {task}")
            elif parsed_args.command == "list":
                tasks = self._service.list_tasks(status=parsed_args.status)
                if not tasks:
                    print("No tasks found.")
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
                    print(f"Task with ID {parsed_args.id} removed.")
            elif parsed_args.command == "mark-done":
                task = self._service.complete_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    print(f"Task completed: {task}")
            elif parsed_args.command == "mark-in-progress":
                task = self._service.begin_task(parsed_args.id)
                if not task:
                    print(f"Error: Task with ID {parsed_args.id} not found.")
                else:
                    print(f"Task started: {task}")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")