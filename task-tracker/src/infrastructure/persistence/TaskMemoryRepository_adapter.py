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
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add(self, description: str) -> Task:
        """Adds a new task to the in-memory store."""
        task = Task(
            id=self._next_id, 
            description=description,
            status=TaskStatusEnum.TODO,
            createdAt=datetime.datetime.now(),
            updatedAt=datetime.datetime.now()
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by its ID from the in-memory store."""
        for task in self._tasks:
            if task.id == task_id:
                return task

    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """Retrieves all tasks from the in-memory store."""
        if status:
            return [task for task in self._tasks if task.status.value == status.value]
        return self._tasks

    def update(self, task: Task) -> Optional[Task]:
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                self._tasks[i] = task
                return task
        return None
    
    def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID from the in-memory store."""
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                return True
        return False