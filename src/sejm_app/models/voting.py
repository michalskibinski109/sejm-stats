from django.db import models
import django
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from loguru import logger
from django.utils.functional import cached_property
from django.conf import settings
from sejm_app.utils import parse_all_dates, camel_to_snake
from sejm_app.models.vote import Vote, ClubVote, VotingOption
from sejm_app.models.club import Club
import re


class Voting(models.Model):
    id = models.IntegerField(primary_key=True, help_text=_("Voting ID"))
    yes = models.SmallIntegerField(null=True, blank=True, help_text=_("Yes votes"))
    no = models.SmallIntegerField(null=True, blank=True, help_text=_("No votes"))
    abstain = models.SmallIntegerField(
        null=True, blank=True, help_text=_("Abstain votes")
    )
    term = models.IntegerField(null=True, blank=True, help_text=_("Sejm term number"))
    sitting = models.IntegerField(
        null=True, blank=True, help_text=_("Number of the Sejm sitting")
    )
    sittingDay = models.IntegerField(
        null=True, blank=True, help_text=_("Day number of the Sejm sitting")
    )
    votingNumber = models.IntegerField(
        null=True, blank=True, help_text=_("Voting number")
    )
    date = models.DateTimeField(null=True, blank=True, help_text=_("Date of the vote"))
    title = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Voting topic")
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Voting description")
    )
    topic = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Short voting topic")
    )

    pdfLink = models.URLField(
        null=True,
        blank=True,
        help_text=_("Link to the PDF document with voting details"),
    )
    kind = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Type of voting, one of ELECTRONIC, TRADITIONAL, ON_LIST"),
    )

    success = models.BooleanField(
        null=True, blank=True, help_text=_("Whether the voting was successful")
    )

    def _check_if_success(self) -> bool:
        if self.no + self.yes + self.abstain < 230:
            logger.warning(
                f"Voting {self.id} has less than 230 votes, cannot determine if passed"
            )
        return self.yes > self.no

    def __str__(self):
        return f"{self.title} ({self.date})"

    @cached_property
    def resolution_urls(self) -> list[str] | None:
        search_str = (self.title or "") + (self.topic or "")
        sub_str = re.search(r"(druki? nr\.? .+)", search_str)
        if not sub_str:
            return None
        sub_str = sub_str.group(1)
        numbers = re.findall(r"\d+(?:-\w)?", sub_str)
        return [f"{settings.RESOLUTION_URL}/{number}_u.htm" for number in numbers]
        # return

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.sitting * 100000 + self.sittingDay * 1000 + self.votingNumber
        self.success = self._check_if_success()
        super().save(*args, **kwargs)
