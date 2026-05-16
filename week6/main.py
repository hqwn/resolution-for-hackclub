import tkinter as tk
from tkinter import messagebox
import os
import json

TASKS_FILE = "tasks.json"
root = tk.Tk()
root.title("To-Do list")
root.geometry("350x350")
root.minsize(250, 250)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
name = tk.Frame()
task_list = tk.Frame()
buttons = tk.Frame()
scrollbar = tk.Scrollbar(task_list)
scrollbar.pack(side="right", fill="y")
listbox = tk.Listbox(task_list, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    
    except json.JSONDecodeError:
        return []

def save_task(task):
    content = load_tasks()
    if content == []:
        id = 1
    else:
        id = content[-1]['id'] + 1
    content.append({"id":id, "task":task})
    
    with open(TASKS_FILE, "w") as file:
        json.dump(content, file, indent=2)
        return {"id":id, "task":task}     

def delete_task():
    task_content = listbox.get(listbox.curselection())
    result = messagebox.askyesno("Confirm", f"Are you sure you want to delete task: {task_content} ?")
    if not result:
        return ''
    content = load_tasks()
    
    for i in content:
        if i['task'] == task_content:
            content.remove(i)
    
    with open(TASKS_FILE, "w") as file:
        json.dump(content, file, indent=2)
    
    update_list() 

def complt_task():
    task_content = listbox.get(listbox.curselection())
    content = load_tasks()
    
    for i in content:
        if i['task'] == task_content:
            i['completed'] = True
    
    with open(TASKS_FILE, "w") as file:
        json.dump(content, file, indent=2)
    
    update_list() 

def pushed():
    if task.get() != '':
        save_task(task.get())
    update_list()

def update_list():
    listbox.delete(0, tk.END)
    for index, i in enumerate(load_tasks()):
        listbox.insert(tk.END, i['task'])

        if 'completed' in i:
            listbox.itemconfig(index, background="lightgreen")
        else:
            listbox.itemconfig(index, background="red")


tk.Label(name, text='Task: ').grid(row=0, column=0)
task = tk.Entry(name)
name.pack(fill="x")
task.grid(row=0, column=1)
add_task = tk.Button(buttons, text='Add Task', command=pushed)
add_task.grid(row=3, column=0, padx=5, pady=5)
del_task = tk.Button(buttons, text='Delete current selected task', command=delete_task)
del_task.grid(row=3, column=1, padx=5, pady=5)
complete_task = tk.Button(buttons, text='Complete current selected task', command=complt_task)
complete_task.grid(row=4, column=0, padx=5, pady=5)


name.grid(row=0, column=0, sticky="ew")
task_list.grid(row=1, column=0, sticky="nsew")
buttons.grid(row=2, column=0, sticky="ew")
update_list()

root.mainloop()
