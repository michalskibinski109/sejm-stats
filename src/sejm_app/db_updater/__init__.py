from .club_updater import ClubUpdaterTask
from .envoy_updater import EnvoyUpdaterTask
from .votings_updater import VotingsUpdaterTask

envoy_upd = EnvoyUpdaterTask()
club_upd = ClubUpdaterTask()
voting_upd = VotingsUpdaterTask()
