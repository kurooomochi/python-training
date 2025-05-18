from  dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import datetime

class TaskStatusEnum(Enum):
    """
    Enumeration for the possible statuses of a Task.
    """
    DONE = "done"
    INPROGRESS = "in progress"
    TODO = "to do"

@dataclass
class Task:
    """
    Represents a single task in the to-do list.

    Attributes:
        description (str): The description of the task.
        status (TaskStatusEnum): The current status of the task.
        createdAt (datetime.datetime): The timestamp when the task was created.
        updatedAt (datetime.datetime): The timestamp when the task was last updated.
        id (Optional[int]): The unique identifier of the task. Defaults to None.
    """
    description: str
    status: TaskStatusEnum
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    id: Optional[int] = field(default=None)

    def mark_as_done(self):
        """Marks the task as done and updates the updatedAt timestamp."""
        self.status = TaskStatusEnum.DONE
        self.updatedAt = datetime.datetime.now()

    def mark_as_todo(self):
        """Marks the task as to-do and updates the updatedAt timestamp."""
        self.status = TaskStatusEnum.TODO
        self.updatedAt = datetime.datetime.now()
    
    def mark_as_inprogress(self):
        """Marks the task as in progress and updates the updatedAt timestamp."""
        self.status = TaskStatusEnum.INPROGRESS
        self.updatedAt = datetime.datetime.now()

    def __str__(self):
        """Returns a string representation of the task."""
        status_icon = "✓" if self.status == TaskStatusEnum.DONE else ("⏳" if self.status == TaskStatusEnum.INPROGRESS else "✗")
        return f"[{status_icon}] ID: {self.id} - {self.description} (Created: {self.createdAt}, Updated: {self.updatedAt})"

