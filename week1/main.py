import argparse
import sys
import os
import json

TASKS_FILE = 'week1/tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-a", "--add", type=int, help="Add notes for a task by ID")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
if args.list:
    tasks = load_tasks()
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['task']}")
    sys.exit(0)

elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        id = 1
    else:
        id = tasks[-1]["id"] + 1
    tasks.append({"id": id, "task": args.task, "done": False})
    save_task(tasks)

    print(f"Task {args.task} added with ID of {id}")

elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break

elif args.delete:
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
        if task['id'] != args.delete:
            new_tasks.append(task)
    tasks = new_tasks
    save_task(new_tasks)
    print(f'Task with ID :{args.delete} deleted')

elif args.add:
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == args.add:
            note = input('Enter your notes: ')
            task['Notes'] = note
    
    save_task(tasks)
    print(f'Added note: {note}, to item with ID {args.add}')
