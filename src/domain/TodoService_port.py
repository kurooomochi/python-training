from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.Task import Task, TaskStatusEnum

class TodoServicePort(ABC):
    """
    Port (Interface) for the To-Do service operations.

    This interface defines the contract for the application's core logic
    related to task management.
    """
    @abstractmethod
    def add_task(self, description: str) -> Task:
        """
        Adds a new task.

        Args:
            description (str): The description of the task.

        Returns:
            Task: The newly created task.
        """
        pass
    
    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a specific task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, otherwise None.
        """
        pass
    
    @abstractmethod
    def list_tasks(self, status: Optional[TaskStatusEnum]) -> List[Task]:
        """
        Lists all tasks, optionally filtered by status.

        Args:
            status (Optional[TaskStatusEnum]): The status to filter tasks by. 
                                              If None, all tasks are returned.

        Returns:
            List[Task]: A list of tasks.
        """
        pass

    @abstractmethod
    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to complete.

        Returns:
            Optional[Task]: The updated task if found and completed, otherwise None.
        """
        pass
    
    @abstractmethod
    def begin_task(self, task_id: int) -> Optional[Task]:
        """
        Marks a task as in progress.

        Args:
            task_id (int): The ID of the task to mark as in progress.

        Returns:
            Optional[Task]: The updated task if found and marked, otherwise None.
        """
        pass

    @abstractmethod
    def remove_task(self, task_id: int) -> bool:
        """
        Removes a task.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed successfully, False otherwise.
        """
        pass