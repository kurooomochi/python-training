from abc import ABC, abstractmethod
from domain.Task import Task, TaskStatusEnum
from typing import Optional, List

class TaskRepositoryPort(ABC):
    @abstractmethod
    def add(self, description: str) -> Task:
        pass
        
    @abstractmethod
    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass
        
    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        pass
        