from task_repository_port import TaskPort
import json

class TaskMemoryRepository(TaskPort):
    def __init__(self):
        self.file_path = 'tasks.json'
        self.tasks = []
    
    def retrieve_tasks_from_json(self):
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
                if content:
                    self.tasks = json.loads(content)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def append_task_to_json(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.tasks, f, indent=4)
            print(f"Task appended to '{self.file_path}' successfully.")
        except IOError:
            print(f"Error: Could not write to '{self.file_path}'.")

    def add_task(self, new_task):
        self.retrieve_tasks_from_json()
        self.tasks.append(new_task)
        

    def delete_task(self, args):
        pass
        # print('removing task...')
        # print(f'task id to remove {args.id}')

    def update_task(self, args, status_to_set=None):
        pass
        # print('updating task...')
        # print(f'task id to update {args.id}')
        # if status_to_set:
        #     print(f'New status: {status_to_set}')

    def list_tasks(state):
        pass

    def show_task_detail(id: int):
        pass