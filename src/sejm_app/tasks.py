from core.celery import app

from sejm_app.db_updater import tasks as sejm_tasks
from eli_app.db_update import tasks as eli_tasks

for task in eli_tasks + sejm_tasks:
    app.register_task(task)
