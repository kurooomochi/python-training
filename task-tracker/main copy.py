import argparse
from task_memory_repository_adapter import TaskMemoryRepository


def main():
    taskService = TaskMemoryRepository()
    
    parser = argparse.ArgumentParser(
        prog="task-tracker",
        description="Task Tracker application",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True, help="Available Commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Adds a new task.")
    parser_add.add_argument("description", type=str, help="Task description.")
    parser_add.set_defaults(func=taskService.add_task)

    # Delete command
    parser_add = subparsers.add_parser("delete", help="Removes a task.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=taskService.delete_task)
    
    # Update command
    parser_add = subparsers.add_parser("update", help="Updates a task.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=taskService.update_task)

    # Mark In Progress
    parser_add = subparsers.add_parser("mark-in-progress", help="Marks a task as In Progress.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=lambda args_obj: taskService.update_task(args_obj, status_to_set="in-progress"))
    
    # Mark Done
    parser_add = subparsers.add_parser("mark-done", help="Marks a task as Done.")
    parser_add.add_argument("id", type=int, help="Task id.")
    parser_add.set_defaults(func=lambda args_obj: taskService.update_task(args_obj, status_to_set="done"))
    

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()