from typing import List, Optional, Dict

from domain.Task import Task, TaskStatusEnum
from domain.TaskRepository_port import TaskRepositoryPort
import datetime

class TaskMemoryRepository(TaskRepositoryPort):
    """
    An in-memory implementation of the TaskRepositoryPort.
    Useful for testing or simple applications where data persistence
    across sessions is not required.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
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
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by its ID from the in-memory store."""
        return self._tasks.get(task_id)

    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """Retrieves all tasks from the in-memory store."""
        if status:
            return [task for task in self._tasks.values() if task.status == status]
        return list(self._tasks.values())

    def update(self, task: Task) -> Optional[Task]:
        """Updates an existing task in the in-memory store."""
        if task.id is not None and task.id in self._tasks:
            self._tasks[task.id] = task
            return task
        return None

    def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID from the in-memory store."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False