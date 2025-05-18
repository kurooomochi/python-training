import unittest
import os  # Added for file operations
from src.infrastructure.persistence.TaskJsonRepository_adapter import TaskJsonRepository
from src.domain.Task import TaskStatusEnum, Task
import datetime

class TestTaskJsonRepository(unittest.TestCase):
    def setUp(self):
        # Determine the path to the tasks.json file that TaskJsonRepository uses.
        # Assumes the test file is in task-tracker/tests/
        # and tasks.json is in task-tracker/data/tasks.json
        current_file_dir = os.path.dirname(os.path.abspath(__file__))  # .../task-tracker/tests
        project_root = os.path.dirname(current_file_dir)  # .../task-tracker/
        self.tasks_json_path = os.path.join(project_root, 'data', 'tasks.json')

        # Ensure the data directory exists (optional, but good practice)
        data_dir = os.path.dirname(self.tasks_json_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Clean up (delete) the tasks.json file before each test.
        # TaskJsonRepository._load() will create a new one with default content if it's missing.
        if os.path.exists(self.tasks_json_path):
            os.remove(self.tasks_json_path)
        
        self.repository = TaskJsonRepository()

    def test_add_task(self):
        task = self.repository.add("Test Task 1")
        self.assertEqual(task.description, "Test Task 1")
        self.assertEqual(task.status, TaskStatusEnum.TODO)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.createdAt)
        self.assertIsNotNone(task.updatedAt)
        if task.id:
            self.assertEqual(self.repository.get_by_id(task.id), task)

    def test_get_by_id(self):
        task1 = self.repository.add("Test Task 1")
        if task1.id:
            retrieved_task = self.repository.get_by_id(task1.id)
            self.assertEqual(retrieved_task, task1)
        self.assertIsNone(self.repository.get_by_id(999))  # Non-existent ID

    def test_get_all_tasks(self):
        self.repository.add("Task 1")
        self.repository.add("Task 2")
        tasks = self.repository.get_all()
        self.assertEqual(len(tasks), 2)

    def test_get_all_tasks_with_status_filter(self):
        self.repository.add("Task 1 Todo")
        task_done = self.repository.add("Task 2 Done")
        task_done.mark_as_done()
        self.repository.update(task_done)
        
        todo_tasks = self.repository.get_all(status=TaskStatusEnum.TODO)
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0].description, "Task 1 Todo")

        done_tasks = self.repository.get_all(status=TaskStatusEnum.DONE)
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].description, "Task 2 Done")
        
        inprogress_tasks = self.repository.get_all(status=TaskStatusEnum.INPROGRESS)
        self.assertEqual(len(inprogress_tasks), 0)

    def test_update_task(self):
        task = self.repository.add("Original Description")
        task.description = "Updated Description"
        task.mark_as_done()
        updated_task = self.repository.update(task)
        self.assertIsNotNone(updated_task, "Updated task should not be None")
        if updated_task:  # Only check attributes if update was successful
            self.assertEqual(updated_task.description, "Updated Description")
            self.assertEqual(updated_task.status, TaskStatusEnum.DONE)

        # Test updating a non-existent task
        non_existent_task = Task(id=999, description="Non Existent", status=TaskStatusEnum.TODO, createdAt=datetime.datetime.now(), updatedAt=datetime.datetime.now())
        self.assertIsNone(self.repository.update(non_existent_task))

    def test_delete_task(self):
        task = self.repository.add("Task to delete")
        if task.id:
            self.assertTrue(self.repository.delete(task.id))
            self.assertIsNone(self.repository.get_by_id(task.id))
        self.assertFalse(self.repository.delete(999))  # Non-existent ID

if __name__ == '__main__':
    unittest.main()
