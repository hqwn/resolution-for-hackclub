from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json

app = FastAPI()

TASKS_FILE = "tasks.json"

class TaskBody(BaseModel):
    task: str

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

@app.get("/")
async def start():
    return {'HI': 'How are You?'}

@app.get("/tasks")
async def load():
    tasks = load_tasks()
    return tasks

@app.get("/tasks/{task_name}")
async def Search_By_TaskName(task_name: str):
    tasks = load_tasks()

    matching_items = []
    for i in tasks:
        if task_name in i["task"]:
            matching_items.append(i)
    
    return matching_items


@app.post("/tasks")
async def add_task(task: TaskBody):
    tasks = load_tasks()
    
    if len(tasks) == 0:
        id = 1
    else:
        id = tasks[-1]['id'] + 1
    
    new_task = {'id': id, "task": task.task, 'done': False}
    tasks.append(new_task)
    save_tasks(tasks)

    return new_task

@app.patch("/tasks/{task_id}/complete")
async def complete(task_id: int):
    tasks = load_tasks()

    for i in tasks:
        if i["id"] == task_id:
            i["done"] = True
            save_tasks(tasks)
            return tasks
    
    raise HTTPException(status_code=404, detail="ID not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()

    for i in tasks:
        if i["id"] == task_id:
            tasks.remove(i)
            save_tasks(tasks)
            return tasks
    
    raise HTTPException(status_code=404, detail="ID not found")

def main():
    import uvicorn
    uvicorn.run("resolution_week3_YOUR_USERNAME.main:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
