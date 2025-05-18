# Task Tracker

This is a simple command-line task tracker application written in Python.

## Features

* Add new tasks
* View existing tasks
* Update task status (e.g., "pending", "in progress", "done")
* Delete tasks
* Tasks are persisted in a JSON file (`data/tasks.json`)

## Project Structure

```
task-tracker/
├── data/
│   └── tasks.json         # Stores task data
├── src/
│   ├── application/
│   │   └── TodoService_adapter.py  # Application service layer
│   ├── domain/
│   │   ├── Task.py                # Task domain model
│   │   ├── TaskRepository_port.py # Port for task repository
│   │   └── TodoService_port.py    # Port for todo service
│   ├── infrastructure/
│   │   ├── cli/
│   │   │   └── handler.py         # Command-line interface handler
│   │   └── persistence/
│   │       ├── TaskJsonRepository_adapter.py # JSON-based task repository
│   │       └── TaskMemoryRepository_adapter.py # In-memory task repository (alternative)
├── tests/                 # Unit tests
└── main.py                # Main entry point of the application
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <repository_url>
    # cd task-tracker
    ```

2.  **Ensure Python is installed.** This project is written in Python.

## Usage

The application is run from the command line.

**Available Commands:**

*   **`add <description>`**: Adds a new task with the given description.
    ```bash
    python3 main.py add "Buy groceries"
    ```

*   **`list`**: Lists all tasks with their ID, description, status, and timestamps.
    ```bash
    python3 main.py list
    ```

*   **`get <task_id>`**: Retrieves and displays a specific task by its ID.
    ```bash
    python3 main.py get 1
    ```

*   **`remove <task_id>`**: Deletes a task by its ID.
    ```bash
    python3 main.py delete 1
    ```

*   **`mark-done <task_id>`**: Marks a task as 'done'.
    ```bash
    python3 main.py mark-done 1
    ```

*   **`mark-in-progress <task_id>`**: Marks a task as 'in progress'.
    ```bash
    python3 main.py mark-in-progress 1
    ```

*   **`mark-todo <task_id>`**: Marks a task as 'to do'.
    ```bash
    python3 main.py mark-todo 1
    ```

## Development

### Running Tests

To run the unit tests, navigate to the `task-tracker` directory and run:

```bash
python -m unittest discover -s tests
```

(You might need to adjust the command based on your Python testing setup if you have one.)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
