from slack_bolt import Ack, Respond
from logging import Logger
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    old_tasks = load_tasks()
    task_id = old_tasks[-1]['task_id'] + 1 if old_tasks else 1
    old_tasks.append({"task_id": task_id, 'task': tasks})
    with open(TASKS_FILE, "w") as file:
        json.dump(old_tasks, file, indent=2)
    
    return task_id

def delete_task(task_id):
    old_tasks = load_tasks()
    
    for i in old_tasks:
        if i['task_id'] == task_id:
            removed_task = i
            old_tasks.remove(i)
            break
    
    if removed_task is None:
        return f"No task found with id {task_id}."

    with open(TASKS_FILE, "w") as file:
        json.dump(old_tasks, file, indent=2)
    
    return f'Removed task {removed_task['task']} with the id of {removed_task["task_id"]}'



def make_task_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        task_id = save_task(command['text'])
        respond(f"Task added: {command['text']} with id of {task_id}")
    except Exception as e:
        logger.error(e)
        respond(f"Something went wrong: {e}")


def get_all_tasks_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        for i in load_tasks():
            respond(f"Task: {i['task']} with id of {i['task_id']}")
    except Exception as e:
        logger.error(e)
        respond(f"Something went wrong: {e}")
    

def delete_task_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        task_id = int(command['text'])
        message = delete_task(task_id)
        respond(message)
    except Exception as e:
        logger.error(e)
        respond(f"Something went wrong: {e}")
