# Simple Python Application - Task Manager

A simple command-line task manager application written in Python.

## Features

- ✅ Add new tasks
- 📋 List all tasks
- ✓ Mark tasks as completed
- 🗑️ Delete tasks
- 💾 Persistent storage using JSON
- 🎨 Clean and intuitive CLI interface

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Switch to the feature branch:
```bash
git checkout feature/test-18
```

## Usage

Run the application:
```bash
python3 app.py
```

### Available Commands

| Command | Description | Example |
|---------|-------------|----------|
| `add <description>` | Add a new task | `add Buy groceries` |
| `list` | List all tasks | `list` |
| `complete <id>` | Mark a task as completed | `complete 1` |
| `delete <id>` | Delete a task | `delete 2` |
| `help` | Show help message | `help` |
| `exit` | Exit the application | `exit` |

### Example Session

```bash
$ python3 app.py

🚀 Welcome to the Simple Python Task Manager!
Type 'help' for available commands.

taskmanager> add Buy groceries
✓ Task added: Buy groceries

taskmanager> add Write documentation
✓ Task added: Write documentation

taskmanager> list

==================================================
TASKS
==================================================
○ [1] Buy groceries
○ [2] Write documentation
==================================================

taskmanager> complete 1
✓ Task 1 marked as completed

taskmanager> list

==================================================
TASKS
==================================================
✓ [1] Buy groceries
○ [2] Write documentation
==================================================

taskmanager> exit
👋 Goodbye!
```

## Data Storage

Tasks are automatically saved to a `tasks.json` file in the current directory. This file is created automatically when you add your first task.

## Code Structure

- **TaskManager Class**: Core functionality for managing tasks
  - `add_task()`: Add a new task
  - `list_tasks()`: Display all tasks
  - `complete_task()`: Mark a task as completed
  - `delete_task()`: Remove a task
  - `load_tasks()`: Load tasks from JSON file
  - `save_tasks()`: Save tasks to JSON file

- **Main Loop**: Interactive command-line interface
  - Input parsing and command routing
  - Error handling
  - User-friendly prompts

## Error Handling

The application includes comprehensive error handling:
- Invalid commands are caught and reported
- JSON parsing errors are handled gracefully
- Invalid task IDs are validated
- Keyboard interrupts (Ctrl+C) are handled cleanly

## License

See the LICENSE file in the repository root.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
