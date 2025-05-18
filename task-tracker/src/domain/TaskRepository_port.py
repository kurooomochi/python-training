from abc import ABC, abstractmethod
from src.domain.Task import Task, TaskStatusEnum
from typing import Optional, List

class TaskRepositoryPort(ABC):
    """
    Port (Interface) for task repository operations.

    This interface defines the contract for any adapter that provides
    task persistence capabilities.
    """
    @abstractmethod
    def add(self, description: str) -> Task:
        """
        Adds a new task with the given description.

        Args:
            description (str): The description of the task.

        Returns:
            Task: The newly created task.
        """
        pass
        
    @abstractmethod
    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """
        Retrieves all tasks, optionally filtered by status.

        Args:
            status (Optional[TaskStatusEnum]): The status to filter tasks by. 
                                              If None, all tasks are returned.

        Returns:
            List[Task]: A list of tasks.
        """
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a task by its unique identifier.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, otherwise None.
        """
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """
        Deletes a task by its unique identifier.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted successfully, False otherwise.
        """
        pass
        
    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        """
        Updates an existing task.

        Args:
            task (Task): The task object with updated information.

        Returns:
            Optional[Task]: The updated task if found and updated, otherwise None.
        """
        pass
