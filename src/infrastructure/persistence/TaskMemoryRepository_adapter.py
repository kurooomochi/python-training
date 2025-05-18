from typing import List, Optional

from src.domain.Task import Task, TaskStatusEnum
from src.domain.TaskRepository_port import TaskRepositoryPort
import datetime

class TaskMemoryRepository(TaskRepositoryPort):
    """
    An in-memory implementation of the TaskRepositoryPort.
    
    Useful for testing or simple applications where data persistence
    across sessions is not required.
    """
    def __init__(self):
        """Initializes the TaskMemoryRepository with an empty list of tasks."""
        self._tasks: List[Task] = []
        self._next_id: int = 1 # Simple counter for unique IDs

    def add(self, description: str) -> Task:
        """Adds a new task to the in-memory store."""
        current_time = datetime.datetime.now()
        task = Task(
            id=self._next_id, 
            description=description,
            status=TaskStatusEnum.TODO,
            createdAt=current_time,
            updatedAt=current_time
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by its ID from the in-memory store."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None # Explicitly return None if not found

    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """Retrieves all tasks from the in-memory store, optionally filtered by status."""
        if status:
            return [task for task in self._tasks if task.status == status] # Direct enum comparison
        return self._tasks

    def update(self, task: Task) -> Optional[Task]: # Changed parameter name to 'task'
        """Updates an existing task in the in-memory store."""
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                task.updatedAt = datetime.datetime.now() # Ensure updatedAt is current
                self._tasks[i] = task
                return task
        return None # Return None if task to update is not found
    
    def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID from the in-memory store."""
        task_to_delete = self.get_by_id(task_id)
        if task_to_delete:
            self._tasks.remove(task_to_delete)
            return True
        return False