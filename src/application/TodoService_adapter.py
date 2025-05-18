from typing import Optional, List
from src.domain.Task import Task, TaskStatusEnum
from src.domain.TodoService_port import TodoServicePort
from src.domain.TaskRepository_port import TaskRepositoryPort

class TodoService(TodoServicePort):
    """
    Adapter for the To-Do service.

    This class implements the TodoServicePort and orchestrates task management
    operations by interacting with a TaskRepositoryPort.
    """
    def __init__(self, repository: TaskRepositoryPort):
        """
        Initializes the TodoService with a task repository.

        Args:
            repository (TaskRepositoryPort): The repository to be used for task persistence.
        """
        self.repository = repository

    def add_task(self, description: str) -> Task:
        """
        Adds a new task.

        Args:
            description (str): The description of the task.

        Returns:
            Task: The newly created task.

        Raises:
            ValueError: If the description is empty or whitespace.
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty.")
        
        return self.repository.add(description=description)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a specific task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, otherwise None.
        """
        return self.repository.get_by_id(task_id)
    
    def list_tasks(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """
        Lists all tasks, optionally filtered by status.

        Args:
            status (Optional[TaskStatusEnum]): The status to filter tasks by. 
                                              If None, all tasks are returned.

        Returns:
            List[Task]: A list of tasks.
        """
        return self.repository.get_all(status=status)

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to complete.

        Returns:
            Optional[Task]: The updated task if found and completed, otherwise None.
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.mark_as_done() # This will also update the updatedAt timestamp
            return self.repository.update(task)
        
        return None
    
    def begin_task(self, task_id: int) -> Optional[Task]:
        """
        Marks a task as in progress.

        Args:
            task_id (int): The ID of the task to mark as in progress.

        Returns:
            Optional[Task]: The updated task if found and marked, otherwise None.
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.mark_as_inprogress() # This will also update the updatedAt timestamp
            return self.repository.update(task)
        
        return None

    def remove_task(self, task_id: int) -> bool:
        """
        Removes a task.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed successfully, False otherwise.
        """
        return self.repository.delete(task_id)