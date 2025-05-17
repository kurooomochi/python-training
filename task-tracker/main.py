# main.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


from src.application.TodoService_adapter import TodoService
from src.infrastructure.persistence.TaskMemoryRepository_adapter import TaskMemoryRepository
from src.infrastructure.cli.handler import CLIHandler

def main():
    """
    Main function to set up and run the To-Do CLI application.
    This is the composition root of the application, where dependencies are wired together.
    """
    # 1. Choose and initialize the Driven Adapter (Persistence)
    task_repository = TaskMemoryRepository()

    # 2. Initialize the Application Core (Service)
    todo_service = TodoService(repository=task_repository)

    # 3. Initialize the Driving Adapter (CLI)
    cli_handler = CLIHandler(service=todo_service)

    # 4. Run the application by letting the CLI handler process command-line arguments
    cli_handler.handle()

if __name__ == "__main__":
    main()