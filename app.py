import json
import os
from datetime import datetime
from typing import List, Dict, Any

class TodoApp:
    def __init__(self, filename: str = "todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_todos(self) -> None:
        """Save todos to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2, default=str)
    
    def add_task(self, task: str, priority: str = "medium") -> None:
        """Add a new task"""
        new_task = {
            "id": len(self.todos) + 1,
            "task": task,
            "completed": False,
            "priority": priority.lower(),
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.todos.append(new_task)
        self.save_todos()
        print(f"✅ Added task: '{task}' with {priority} priority")
    
    def view_tasks(self, show_completed: bool = False) -> None:
        """Display all tasks"""
        if not self.todos:
            print("📝 No tasks found!")
            return
        
        print("\n" + "="*50)
        print("📋 YOUR TODO LIST")
        print("="*50)
        
        # Filter tasks based on completion status
        tasks_to_show = self.todos if show_completed else [t for t in self.todos if not t['completed']]
        
        if not tasks_to_show:
            status = "completed" if not show_completed else "pending"
            print(f"No {status} tasks found!")
            return
        
        # Sort by priority (high -> medium -> low)
        priority_order = {"high": 1, "medium": 2, "low": 3}
        tasks_to_show.sort(key=lambda x: priority_order.get(x['priority'], 2))
        
        for task in tasks_to_show:
            status = "✅" if task['completed'] else "⏳"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            priority_icon = priority_emoji.get(task['priority'], "🟡")
            
            print(f"{status} [{task['id']}] {priority_icon} {task['task']}")
            if task['completed'] and task['completed_at']:
                completed_date = datetime.fromisoformat(task['completed_at']).strftime("%Y-%m-%d %H:%M")
                print(f"    Completed: {completed_date}")
        
        print("="*50)
    
    def complete_task(self, task_id: int) -> None:
        """Mark a task as completed"""
        for task in self.todos:
            if task['id'] == task_id:
                if task['completed']:
                    print(f"⚠️  Task '{task['task']}' is already completed!")
                else:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().isoformat()
                    self.save_todos()
                    print(f"🎉 Completed task: '{task['task']}'")
                return
        print(f"❌ Task with ID {task_id} not found!")
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task"""
        for i, task in enumerate(self.todos):
            if task['id'] == task_id:
                deleted_task = self.todos.pop(i)
                self.save_todos()
                print(f"🗑️  Deleted task: '{deleted_task['task']}'")
                return
        print(f"❌ Task with ID {task_id} not found!")
    
    def get_stats(self) -> None:
        """Display todo statistics"""
        total = len(self.todos)
        completed = len([t for t in self.todos if t['completed']])
        pending = total - completed
        
        print("\n" + "="*30)
        print("📊 TODO STATISTICS")
        print("="*30)
        print(f"Total tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Completion rate: {completion_rate:.1f}%")
        print("="*30)

def main():
    """Main application loop"""
    app = TodoApp()
    
    print("🎯 Welcome to Python Todo App!")
    print("Type 'help' for available commands")
    
    while True:
        try:
            command = input("\n📝 Enter command: ").strip().lower()
            
            if command == 'help':
                print("\n📚 Available commands:")
                print("  add <task> [priority]  - Add a new task (priority: high/medium/low)")
                print("  list                   - Show pending tasks")
                print("  list all              - Show all tasks (including completed)")
                print("  complete <id>         - Mark task as completed")
                print("  delete <id>           - Delete a task")
                print("  stats                 - Show statistics")
                print("  help                  - Show this help message")
                print("  quit                  - Exit the application")
            
            elif command.startswith('add '):
                parts = command[4:].split()
                if not parts:
                    print("❌ Please provide a task description!")
                    continue
                
                # Check if last word is a priority
                priorities = ['high', 'medium', 'low']
                if len(parts) > 1 and parts[-1] in priorities:
                    priority = parts[-1]
                    task = ' '.join(parts[:-1])
                else:
                    priority = 'medium'
                    task = ' '.join(parts)
                
                app.add_task(task, priority)
            
            elif command == 'list':
                app.view_tasks(show_completed=False)
            
            elif command == 'list all':
                app.view_tasks(show_completed=True)
            
            elif command.startswith('complete '):
                try:
                    task_id = int(command[9:])
                    app.complete_task(task_id)
                except ValueError:
                    print("❌ Please provide a valid task ID!")
            
            elif command.startswith('delete '):
                try:
                    task_id = int(command[7:])
                    app.delete_task(task_id)
                except ValueError:
                    print("❌ Please provide a valid task ID!")
            
            elif command == 'stats':
                app.get_stats()
            
            elif command in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Python Todo App!")
                break
            
            elif command == '':
                continue
            
            else:
                print("❌ Unknown command! Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Python Todo App!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
     