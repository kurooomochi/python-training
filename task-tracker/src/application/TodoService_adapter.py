from typing import Optional, List
from domain.Task import Task, TaskStatusEnum
from domain.TodoService_port import TodoServicePort
from domain.TaskRepository_port import TaskRepositoryPort

class TodoService(TodoServicePort):
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def add_task(self, description: str) -> Task:
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty.")
        
        return self.repository.add(description=description)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repository.get_by_id(task_id)
    
    def list_tasks(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        return self.repository.get_all(status=status)

    def complete_task(self, task_id: int) -> Optional[Task]:
        task = self.repository.get_by_id(task_id)
        if task:
            task.mark_as_done()
            return self.repository.update(task)
        
        return None
    
    def begin_task(self, task_id: int) -> Optional[Task]:
        task = self.repository.get_by_id(task_id)
        if task:
            task.mark_as_inprogress()
            return self.repository.update(task)
        
        return None

    def remove_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)