import json
import os

from src.domain.Task import Task, TaskStatusEnum
from src.domain.TaskRepository_port import TaskRepositoryPort

from typing import Optional, List, Dict
import datetime

class TaskJsonRepository(TaskRepositoryPort):
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self.file_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/tasks.json'))
        self._load()
    
    def _load(self):
        """Loads tasks from the JSON file if it exists."""
        if not os.path.exists(self.file_path):
            # Create an empty file with an empty list if it doesn't exist
            with open(self.file_path, 'w') as f:
                json.dump({"tasks": [], "next_id": 1}, f)

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                loaded_tasks = []
                for task_data in data.get("tasks", []):
                    task = Task(
                        id=task_data.get('id'),
                        description=task_data.get('description'),
                        status=TaskStatusEnum(task_data.get('status', TaskStatusEnum.INPROGRESS.value)),
                        createdAt=datetime.datetime.fromisoformat(task_data.get('createdAt')),
                        updatedAt=datetime.datetime.fromisoformat(task_data.get('updatedAt'))
                    )
                    loaded_tasks.append(task)
                self._tasks = loaded_tasks
                self._next_id = data.get("next_id", 1)
        except (IOError, json.JSONDecodeError):
            # If file is corrupted or not found, start fresh
            self._tasks = []
            self._next_id = 1
            # Consider logging this error in a real application
            print(f"Warning: Could not load tasks from {self.file_path}. Starting fresh.")

    def _save(self):
        """Saves the current state of tasks to the JSON file."""
        try:
            # Convert Task objects to dictionaries
            serializable_tasks = []
            for task in self._tasks:
                serializable_tasks.append({
                    "id": task.id,
                    "description": task.description,
                    "status": task.status.value,
                    "createdAt": task.createdAt.isoformat(),
                    "updatedAt": task.updatedAt.isoformat()
                })
        
            with open(self.file_path, 'w') as f:
                json.dump({"tasks": serializable_tasks, "next_id": self._next_id}, f, indent=4)
        except IOError:
            print(f"Error: Could not save tasks to {self.file_path}.")
    
    def add(self, description: str) -> Task:
        task = Task(
            id= self._next_id,
            description=description,
            createdAt=datetime.datetime.now(),
            updatedAt=datetime.datetime.now(),
            status=TaskStatusEnum.TODO
        )
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task
        
    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        if status:
            return [task for task in self._tasks if task.status.value == status.value]
        return self._tasks

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task

    def delete(self, task_id: int) -> bool:
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                self._save()
                return True
        return False
        
    def update(self, task: Task) -> Optional[Task]:
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                self._tasks[i] = task
                self._save()
                return task
        return None