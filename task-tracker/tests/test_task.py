import unittest
import datetime
from src.domain.Task import Task, TaskStatusEnum

class TestTask(unittest.TestCase):
    def test_task_creation(self):
        now = datetime.datetime.now()
        task = Task(description="Test Task", status=TaskStatusEnum.TODO, createdAt=now, updatedAt=now, id=1)
        self.assertEqual(task.description, "Test Task")
        self.assertEqual(task.status, TaskStatusEnum.TODO)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.createdAt, now)
        self.assertEqual(task.updatedAt, now)

    def test_mark_as_done(self):
        now = datetime.datetime.now()
        task = Task(description="Test Task", status=TaskStatusEnum.TODO, createdAt=now, updatedAt=now)
        task.mark_as_done()
        self.assertEqual(task.status, TaskStatusEnum.DONE)

    def test_mark_as_todo(self):
        now = datetime.datetime.now()
        task = Task(description="Test Task", status=TaskStatusEnum.DONE, createdAt=now, updatedAt=now)
        task.mark_as_todo()
        self.assertEqual(task.status, TaskStatusEnum.TODO)

    def test_mark_as_inprogress(self):
        now = datetime.datetime.now()
        task = Task(description="Test Task", status=TaskStatusEnum.TODO, createdAt=now, updatedAt=now)
        task.mark_as_inprogress()
        self.assertEqual(task.status, TaskStatusEnum.INPROGRESS)

    def test_task_str_representation(self):
        now = datetime.datetime.now()
        task_todo = Task(description="Todo Task", status=TaskStatusEnum.TODO, createdAt=now, updatedAt=now, id=1)
        self.assertEqual(str(task_todo), "[✗] ID: 1 - Todo Task")

        task_done = Task(description="Done Task", status=TaskStatusEnum.DONE, createdAt=now, updatedAt=now, id=2)
        # Simulate the string representation for a done task
        # The actual character might differ based on implementation, this is a common representation
        self.assertEqual(str(task_done), "[✓] ID: 2 - Done Task")

if __name__ == '__main__':
    unittest.main()
