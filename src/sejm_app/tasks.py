from core.celery import app

from sejm_app.db_updater import tasks

for task in tasks:
    app.register_task(task)
