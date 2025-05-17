from  dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import datetime

class TaskStatusEnum(Enum):
    DONE = "done"
    INPROGRESS = "in progress"
    TODO = "to do"

@dataclass
class Task:
    """
    Represents a single task in the to-do list
    """
    description: str
    status: TaskStatusEnum
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    id: Optional[int] = field(default=None)

    def mark_as_done(self):
        self.status = TaskStatusEnum.DONE

    def mark_as_todo(self):
        self.status = TaskStatusEnum.TODO
    
    def mark_as_inprogress(self):
        self.status = TaskStatusEnum.INPROGRESS

    def __str__(self):
        status = "✓" if self.status == TaskStatusEnum.DONE else "✗"
        return f"[{status}] ID: {self.id} - {self.description}"

