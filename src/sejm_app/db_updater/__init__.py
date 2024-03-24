from .db_updater_task import DbUpdaterTask
from .club_updater import ClubUpdaterTask
from .envoy_updater import EnvoyUpdaterTask
from .votings_updater import VotingsUpdaterTask
from .prints_updater import PrintsUpdaterTask
from .interpellations_updater import InterpellationsUpdaterTask
from .processes_updater import ProcessesUpdaterTask
from .committees_updater import CommitteeUpdaterTask

tasks = (
    ClubUpdaterTask(),
    EnvoyUpdaterTask(),
    VotingsUpdaterTask(),
    PrintsUpdaterTask(),
    InterpellationsUpdaterTask(),
    ProcessesUpdaterTask(),
    CommitteeUpdaterTask(),
)
