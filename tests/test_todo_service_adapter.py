import unittest
from unittest.mock import MagicMock
from src.application.TodoService_adapter import TodoService
from src.domain.Task import Task, TaskStatusEnum
from src.domain.TaskRepository_port import TaskRepositoryPort
import datetime

class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=TaskRepositoryPort)
        self.service = TodoService(repository=self.mock_repository)
        self.now = datetime.datetime.now()

    def _create_sample_task(self, id=1, description="Test Task", status=TaskStatusEnum.TODO):
        return Task(id=id, description=description, status=status, createdAt=self.now, updatedAt=self.now)

    def test_add_task(self):
        sample_task = self._create_sample_task(description="New Task")
        self.mock_repository.add.return_value = sample_task
        
        task = self.service.add_task("New Task")
        self.mock_repository.add.assert_called_once_with(description="New Task")
        self.assertEqual(task, sample_task)

    def test_add_task_empty_description(self):
        with self.assertRaises(ValueError) as context:
            self.service.add_task("")
        self.assertEqual(str(context.exception), "Task description cannot be empty.")
        
        with self.assertRaises(ValueError) as context:
            self.service.add_task("   ") # Whitespace only
        self.assertEqual(str(context.exception), "Task description cannot be empty.")
        self.mock_repository.add.assert_not_called()

    def test_get_task(self):
        sample_task = self._create_sample_task(id=1)
        self.mock_repository.get_by_id.return_value = sample_task
        
        task = self.service.get_task(1)
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.assertEqual(task, sample_task)

    def test_get_task_not_found(self):
        self.mock_repository.get_by_id.return_value = None
        task = self.service.get_task(99)
        self.mock_repository.get_by_id.assert_called_once_with(99)
        self.assertIsNone(task)

    def test_list_tasks_no_filter(self):
        tasks_list = [self._create_sample_task(id=1), self._create_sample_task(id=2, description="Another Task")]
        self.mock_repository.get_all.return_value = tasks_list
        
        tasks = self.service.list_tasks()
        self.mock_repository.get_all.assert_called_once_with(status=None)
        self.assertEqual(tasks, tasks_list)

    def test_list_tasks_with_status_filter(self):
        tasks_list = [self._create_sample_task(id=1, status=TaskStatusEnum.DONE)]
        self.mock_repository.get_all.return_value = tasks_list
        
        tasks = self.service.list_tasks(status=TaskStatusEnum.DONE)
        self.mock_repository.get_all.assert_called_once_with(status=TaskStatusEnum.DONE)
        self.assertEqual(tasks, tasks_list)

    def test_complete_task(self):
        original_task = self._create_sample_task(id=1, status=TaskStatusEnum.TODO)
        # When get_by_id is called, return the original task
        self.mock_repository.get_by_id.return_value = original_task
        
        # Mock the update method to return the task that would be saved
        # This simulates the task being updated and returned by the repository
        def side_effect_update(task_to_update):
            self.assertEqual(task_to_update.status, TaskStatusEnum.DONE) # Check if status was changed
            return task_to_update

        self.mock_repository.update.side_effect = side_effect_update
        
        completed_task = self.service.complete_task(1)
        
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once_with(original_task)
        self.assertIsNotNone(completed_task)
        if completed_task:
            self.assertEqual(completed_task.status, TaskStatusEnum.DONE)

    def test_complete_task_not_found(self):
        self.mock_repository.get_by_id.return_value = None
        task = self.service.complete_task(99)
        self.mock_repository.get_by_id.assert_called_once_with(99)
        self.mock_repository.update.assert_not_called()
        self.assertIsNone(task)

    def test_begin_task(self):
        original_task = self._create_sample_task(id=1, status=TaskStatusEnum.TODO)
        self.mock_repository.get_by_id.return_value = original_task

        def side_effect_update(task_to_update):
            self.assertEqual(task_to_update.status, TaskStatusEnum.INPROGRESS)
            return task_to_update
        
        self.mock_repository.update.side_effect = side_effect_update

        in_progress_task = self.service.begin_task(1)

        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once_with(original_task)
        self.assertIsNotNone(in_progress_task)
        if in_progress_task:
            self.assertEqual(in_progress_task.status, TaskStatusEnum.INPROGRESS)

    def test_begin_task_not_found(self):
        self.mock_repository.get_by_id.return_value = None
        task = self.service.begin_task(99)
        self.mock_repository.get_by_id.assert_called_once_with(99)
        self.mock_repository.update.assert_not_called()
        self.assertIsNone(task)

    def test_remove_task(self):
        self.mock_repository.delete.return_value = True
        result = self.service.remove_task(1)
        self.mock_repository.delete.assert_called_once_with(1)
        self.assertTrue(result)

    def test_remove_task_not_found(self):
        self.mock_repository.delete.return_value = False
        result = self.service.remove_task(99)
        self.mock_repository.delete.assert_called_once_with(99)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
