from abc import ABC, abstractmethod
from typing import Optional, List
from domain.Task import Task, TaskStatusEnum

class TodoServicePort(ABC):
    @abstractmethod
    def add_task(self, description: str) -> Task:
        pass
    
    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        pass
    
    @abstractmethod
    def list_tasks(self, status: Optional[TaskStatusEnum]) -> List[Task]:
        pass

    @abstractmethod
    def complete_task(self, task_id: int) -> Optional[Task]:
        pass
    
    @abstractmethod
    def begin_task(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def remove_task(self, task_id: int) -> bool:
        pass