from abc import ABC, abstractmethod

class TaskPort(ABC):
    @abstractmethod
    def add_task(self, args):
        pass
        
    @abstractmethod
    def delete_task(self, args):
        pass
        
    @abstractmethod
    def update_task(self, args, status_to_set=None):
        pass
        
    @abstractmethod
    def list_tasks(state):
        pass

    @abstractmethod
    def show_task_detail(id: int):
        pass