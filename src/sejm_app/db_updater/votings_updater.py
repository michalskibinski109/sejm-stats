from django.conf import settings
from loguru import logger
import requests
from sejm_app import models
from django.db.models import Model
from django.db import transaction
from sejm_app.models import Voting, Vote, ClubVote, VotingOption, Club

from .db_updater_task import DbUpdaterTask


class VotingsUpdaterTask(DbUpdaterTask):
    MODEL: Model = models.Voting
    DATE_FIELD_NAME = "date"

    def run(self, *args, **kwargs):
        logger.info("Updating votings")

        self._download_votings()

    def _get_sitting_and_number(self):
        last_voting = (
            Voting.objects.order_by("-date").first()
            if Voting.objects.exists()
            else None
        )
        sitting, number = (
            (last_voting.sitting, last_voting.votingNumber + 1)
            if last_voting
            else (1, 1)
        )
        return sitting, number

    def _create_club_votes(self, voting: Voting):
        for club in Club.objects.all():
            if voting.club_votes.filter(club=club).exists():
                continue
            votes = Vote.objects.filter(voting=voting, MP__club=club)
            yes = votes.filter(vote=VotingOption.YES).count()
            no = votes.filter(vote=VotingOption.NO).count()
            abstain = votes.filter(
                vote__in=[VotingOption.ABSTAIN, VotingOption.ABSENT]
            ).count()
            club_vote = ClubVote.objects.create(
                club=club, voting=voting, yes=yes, no=no, abstain=abstain
            )
            club_vote.save()

    def _download_votings(self):
        sitting, number = self._get_sitting_and_number()
        logger.info(f"Downloading votings from {sitting} sitting")
        while number < 1000:  # 1000 is a random number, we need to stop at some point
            resp = requests.get(f"{settings.VOTINGS_URL}/{sitting}/{number}")
            logger.debug(f"Downloaded voting {sitting}/{number}: {resp.status_code}")
            if resp.status_code == 404 and number > 1:
                sitting += 1
                number = 1
                continue
            if resp.status_code == 404 or resp.json() == []:
                logger.info(f"Finished downloading votings from {sitting} sitting")
                break
            resp.raise_for_status()
            with transaction.atomic():
                voting = Voting.from_api_response(resp.json())
                self._create_club_votes(voting)
            number += 1
