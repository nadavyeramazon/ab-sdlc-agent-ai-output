#!/usr/bin/env python3
"""Simple Python Application - A basic task manager"""

import json
import os
from datetime import datetime


class TaskManager:
    """A simple task manager to add, list, and complete tasks."""
    
    def __init__(self, filename='tasks.json'):
        """Initialize the task manager.
        
        Args:
            filename (str): The file to store tasks
        """
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from the JSON file.
        
        Returns:
            list: List of tasks
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.filename}. Starting fresh.")
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description):
        """Add a new task.
        
        Args:
            description (str): Task description
        """
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {description}")
    
    def list_tasks(self):
        """List all tasks."""
        if not self.tasks:
            print("No tasks found. Add a task to get started!")
            return
        
        print("\n" + "="*50)
        print("TASKS")
        print("="*50)
        
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            task_id = task['id']
            description = task['description']
            print(f"{status} [{task_id}] {description}")
        
        print("="*50 + "\n")
    
    def complete_task(self, task_id):
        """Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to complete
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().isoformat()
                self.save_tasks()
                print(f"✓ Task {task_id} marked as completed")
                return
        print(f"✗ Task {task_id} not found")
    
    def delete_task(self, task_id):
        """Delete a task.
        
        Args:
            task_id (int): The ID of the task to delete
        """
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Task deleted: {deleted_task['description']}")
                return
        print(f"✗ Task {task_id} not found")


def print_help():
    """Print help information."""
    print("""
╔═══════════════════════════════════════════════════════╗
║         Simple Python Task Manager                    ║
╚═══════════════════════════════════════════════════════╝

Commands:
  add <description>     Add a new task
  list                  List all tasks
  complete <id>         Mark a task as completed
  delete <id>           Delete a task
  help                  Show this help message
  exit                  Exit the application

Examples:
  add Buy groceries
  list
  complete 1
  delete 2
    """)


def main():
    """Main application loop."""
    print("\n🚀 Welcome to the Simple Python Task Manager!")
    print("Type 'help' for available commands.\n")
    
    task_manager = TaskManager()
    
    while True:
        try:
            user_input = input("taskmanager> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command == 'exit' or command == 'quit':
                print("👋 Goodbye!")
                break
            
            elif command == 'help':
                print_help()
            
            elif command == 'list':
                task_manager.list_tasks()
            
            elif command == 'add':
                if len(parts) < 2:
                    print("✗ Usage: add <description>")
                else:
                    task_manager.add_task(parts[1])
            
            elif command == 'complete':
                if len(parts) < 2:
                    print("✗ Usage: complete <task_id>")
                else:
                    try:
                        task_id = int(parts[1])
                        task_manager.complete_task(task_id)
                    except ValueError:
                        print("✗ Task ID must be a number")
            
            elif command == 'delete':
                if len(parts) < 2:
                    print("✗ Usage: delete <task_id>")
                else:
                    try:
                        task_id = int(parts[1])
                        task_manager.delete_task(task_id)
                    except ValueError:
                        print("✗ Task ID must be a number")
            
            else:
                print(f"✗ Unknown command: {command}")
                print("Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"✗ Error: {str(e)}")


if __name__ == '__main__':
    main()
