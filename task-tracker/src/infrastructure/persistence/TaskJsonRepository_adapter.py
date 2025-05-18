import json
import os

from src.domain.Task import Task, TaskStatusEnum
from src.domain.TaskRepository_port import TaskRepositoryPort

from typing import Optional, List, Dict
import datetime

class TaskJsonRepository(TaskRepositoryPort):
    """
    A JSON file-based implementation of the TaskRepositoryPort.

    This repository stores tasks in a JSON file, providing persistence
    across application sessions.

    Attributes:
        file_path (str): The path to the JSON file used for storage.
    """
    def __init__(self, file_path: Optional[str] = None):
        """
        Initializes the TaskJsonRepository.

        Args:
            file_path (Optional[str]): The path to the JSON file. 
                                       If None, a default path ('data/tasks.json') is used.
        """
        self._tasks: List[Task] = []
        self._next_id: int = 1
        # Default file path if not provided
        self.file_path: str = file_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/tasks.json'))
        
        # Ensure the directory for the JSON file exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        self._load()
    
    def _load(self):
        """Loads tasks from the JSON file if it exists, otherwise creates an empty file."""
        if not os.path.exists(self.file_path):
            # Create an empty file with an empty list and next_id if it doesn't exist
            with open(self.file_path, 'w') as f:
                json.dump({"tasks": [], "next_id": 1}, f, indent=4)
            self._tasks = []
            self._next_id = 1
            return

        try:
            with open(self.file_path, 'r') as f:
                # Handle empty file case
                content = f.read()
                if not content:
                    data = {"tasks": [], "next_id": 1}
                else:
                    data = json.loads(content)
                
                loaded_tasks = []
                for task_data in data.get("tasks", []):
                    # Ensure all necessary fields are present and handle potential errors
                    try:
                        task = Task(
                            id=task_data.get('id'),
                            description=task_data.get('description', 'No description'), # Default description
                            status=TaskStatusEnum(task_data.get('status', TaskStatusEnum.TODO.value)), # Default status
                            createdAt=datetime.datetime.fromisoformat(task_data.get('createdAt', datetime.datetime.now().isoformat())),
                            updatedAt=datetime.datetime.fromisoformat(task_data.get('updatedAt', datetime.datetime.now().isoformat()))
                        )
                        loaded_tasks.append(task)
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Skipping malformed task data: {task_data}. Error: {e}")
                self._tasks = loaded_tasks
                self._next_id = data.get("next_id", 1)
        except (IOError, json.JSONDecodeError) as e:
            # If file is corrupted or other IO error, start fresh
            print(f"Warning: Could not load tasks from {self.file_path}. Error: {e}. Starting fresh.")
            self._tasks = []
            self._next_id = 1
            # Attempt to create a fresh file if loading failed badly
            with open(self.file_path, 'w') as f:
                json.dump({"tasks": [], "next_id": 1}, f, indent=4)

    def _save(self):
        """Saves the current state of tasks to the JSON file."""
        try:
            # Convert Task objects to dictionaries for JSON serialization
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
        except IOError as e:
            print(f"Error: Could not save tasks to {self.file_path}. Error: {e}")
    
    def add(self, description: str) -> Task:
        """Adds a new task to the JSON file."""
        current_time = datetime.datetime.now()
        task = Task(
            id= self._next_id,
            description=description,
            createdAt=current_time,
            updatedAt=current_time,
            status=TaskStatusEnum.TODO
        )
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task
        
    def get_all(self, status: Optional[TaskStatusEnum] = None) -> List[Task]:
        """Retrieves all tasks from the JSON file, optionally filtered by status."""
        if status:
            return [task for task in self._tasks if task.status == status] # Direct enum comparison
        return self._tasks

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by its ID from the JSON file."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None # Explicitly return None if not found

    def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID from the JSON file."""
        task_to_delete = self.get_by_id(task_id)
        if task_to_delete:
            self._tasks.remove(task_to_delete)
            self._save()
            return True
        return False
        
    def update(self, task: Task) -> Optional[Task]:
        """Updates an existing task in the JSON file."""
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                task.updatedAt = datetime.datetime.now() # Ensure updatedAt is current
                self._tasks[i] = task
                self._save()
                return task
        return None