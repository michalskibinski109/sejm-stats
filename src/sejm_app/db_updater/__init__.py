from .club_updater import ClubUpdaterTask
from .envoy_updater import EnvoyUpdaterTask
from .votings_updater import VotingsUpdaterTask
from .prints_updater import PrintsUpdaterTask
from .interpellations_updater import InterpellationsUpdaterTask

tasks = (
    ClubUpdaterTask(),
    EnvoyUpdaterTask(),
    VotingsUpdaterTask(),
    PrintsUpdaterTask(),
    InterpellationsUpdaterTask(),
)
