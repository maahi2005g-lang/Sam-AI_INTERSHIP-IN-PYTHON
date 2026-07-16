import json
import os
from datetime import datetime

JSON_FILE = "tasks.json"


def init_json():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_tasks():
    init_json()
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def valid_date(date_str):
    if not date_str:
        return True  # optional field
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task():
    tasks = load_tasks()

    name = input("Enter task description: ").strip()
    if not name:
        print("Task description cannot be empty.\n")
        return

    priority = input("Enter priority (High/Medium/Low) [Medium]: ").strip().capitalize()
    if priority not in ("High", "Medium", "Low"):
        priority = "Medium"

    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    if not valid_date(due_date):
        print("Invalid date format ignored.")
        due_date = ""

    task = {
        "id": next_id(tasks),
        "task": name,
        "priority": priority,
        "due_date": due_date,
        "status": "Pending",
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added with ID {task['id']}.\n")


def get_valid_id(prompt, tasks):
    """Safely reads and validates a task ID from user input."""
    raw = input(prompt).strip()
    if not raw.isdigit():
        print("Invalid ID. Please enter a number.\n")
        return None
    task_id = int(raw)
    if not any(t["id"] == task_id for t in tasks):
        print("Task ID not found.\n")
        return None
    return task_id


def edit_task():
    tasks = load_tasks()
    display_tasks(tasks)
    if not tasks:
        return

    task_id = get_valid_id("Enter the ID of the task to edit: ", tasks)
    if task_id is None:
        return

    for t in tasks:
        if t["id"] == task_id:
            print("Leave a field blank to keep it unchanged.")
            new_name = input(f"Task [{t['task']}]: ").strip()
            new_priority = input(f"Priority [{t['priority']}]: ").strip().capitalize()
            new_due = input(f"Due Date [{t['due_date']}]: ").strip()

            if new_name:
                t["task"] = new_name
            if new_priority in ("High", "Medium", "Low"):
                t["priority"] = new_priority
            elif new_priority:
                print("Invalid priority ignored.")
            if new_due:
                if valid_date(new_due):
                    t["due_date"] = new_due
                else:
                    print("Invalid date ignored.")

            save_tasks(tasks)
            print("Task updated.\n")
            return


def delete_task():
    tasks = load_tasks()
    display_tasks(tasks)
    if not tasks:
        return

    task_id = get_valid_id("Enter the ID of the task to delete: ", tasks)
    if task_id is None:
        return

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print("Task deleted.\n")


def mark_completed():
    tasks = load_tasks()
    display_tasks(tasks)
    if not tasks:
        return

    task_id = get_valid_id("Enter the ID of the task to mark completed: ", tasks)
    if task_id is None:
        return

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Completed"
    save_tasks(tasks)
    print("Task marked as completed.\n")


def display_tasks(tasks=None):
    if tasks is None:
        tasks = load_tasks()

    if not tasks:
        print("\nNo tasks found.\n")
        return

    print("\n{:<4} {:<30} {:<10} {:<12} {:<10}".format(
        "ID", "Task", "Priority", "Due Date", "Status"))
    print("-" * 70)
    for t in tasks:
        print("{:<4} {:<30} {:<10} {:<12} {:<10}".format(
            t["id"], t["task"][:30], t["priority"], t["due_date"], t["status"]))
    print()


def display_pending_and_completed():
    tasks = load_tasks()
    pending = [t for t in tasks if t["status"] == "Pending"]
    completed = [t for t in tasks if t["status"] == "Completed"]

    print("\n===== PENDING TASKS =====")
    display_tasks(pending) if pending else print("No pending tasks.\n")

    print("===== COMPLETED TASKS =====")
    display_tasks(completed) if completed else print("No completed tasks.\n")


def todo_menu():
    while True:
        print("===== DAILY TASK MANAGER =====")
        print("1. Add Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. Mark Task as Completed")
        print("5. View All Tasks")
        print("6. View Pending & Completed")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            edit_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            mark_completed()
        elif choice == "5":
            display_tasks()
        elif choice == "6":
            display_pending_and_completed()
        elif choice == "7":
            print("Exiting To-Do List. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1-7.\n")


# Run the To-Do List app
todo_menu()
