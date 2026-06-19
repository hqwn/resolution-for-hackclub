from slack_bolt import App
from .commands import make_task_callback, get_all_tasks_callback, delete_task_callback


def register(app: App):
    app.command("/make-task")(make_task_callback)
    app.command("/all-tasks")(get_all_tasks_callback)
    app.command("/delete-task")(delete_task_callback)
