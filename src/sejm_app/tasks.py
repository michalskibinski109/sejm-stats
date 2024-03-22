from core.celery import app

from sejm_app.db_updater import *

app.register_task(club_upd)
app.register_task(envoy_upd)
app.register_task(voting_upd)
tasks = [club_upd, envoy_upd, voting_upd]
