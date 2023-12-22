from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from loguru import logger
from django.utils.functional import cached_property
from django.conf import settings
from sejm_app.utils import parse_all_dates, camel_to_snake
from sejm_app.models.vote import Vote
import re


class Voting(models.Model):
    yes = models.SmallIntegerField(null=True, blank=True, help_text=_("Yes votes"))
    no = models.SmallIntegerField(null=True, blank=True, help_text=_("No votes"))
    abstain = models.SmallIntegerField(
        null=True, blank=True, help_text=_("Abstain votes")
    )

    sitting = models.IntegerField(
        null=True, blank=True, help_text=_("Number of the Sejm sitting")
    )
    sitting_day = models.IntegerField(
        null=True, blank=True, help_text=_("Day number of the Sejm sitting")
    )
    voting_number = models.IntegerField(
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
    pdf_link = models.URLField(
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

    @cached_property
    def success(self) -> bool:
        """
        https://orka.sejm.gov.pl/wydbas.nsf/0/B5FA668643E89D51C1257F03002F9D51/$File/Strony%20odwyklady-3.pdf
        Tak więc dla ważności większości
        rozstrzygnięć konieczny jest udział w głosowaniu
        na sali plenarnej co najmniej 230 posłów. Wyjątkiem są głosowania niezależne od kworum, kiedy
        to Sejm rozstrzyga większością głosów obecnych
        posłów. Dotyczą one, zgodnie z art. 184 ust. 4 regulaminu Sejmu, wniosków formalnych w  sprawie zamknięcia listy mówców, zamknięcia dyskusji, ograniczenia czasu przemówień, stwierdzenia
        kworum i  przeliczenia głosów oraz odroczenia
        dyskusji (art. 184 ust. 7 regulaminu Sejmu). W tych
        wypadkach Sejm może podjąć decyzję niezależnie
        od tego, ilu posłów w momencie głosowania bierze
        w nim udział.
        """
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
        # return f"{settings.RESOLUTION_URL}/{number}_u.htm"
        return [f"{settings.RESOLUTION_URL}/{number}_u.htm" for number in numbers]
        # return

    @classmethod
    def from_api_response(cls, response: dict):
        voting = cls()
        response = parse_all_dates(response)
        response = {camel_to_snake(key): value for key, value in response.items()}
        for key, value in response.items():
            if not hasattr(voting, key):
                logger.debug(f"Voting has no attribute {key}")
                continue
            if key == "votes":
                voting.save()
                votes = (
                    Vote.from_api_response(vote_data, voting) for vote_data in value
                )
                continue
            setattr(voting, key, value)
        voting.save()
        return voting
