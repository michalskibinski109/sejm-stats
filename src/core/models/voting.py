from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from loguru import logger


class Voting(models.Model):
    yes = models.SmallIntegerField(null=True, blank=True, help_text=_("Yes votes"))
    no = models.SmallIntegerField(null=True, blank=True, help_text=_("No votes"))
    abstain = models.SmallIntegerField(
        null=True, blank=True, help_text=_("Abstain votes")
    )

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
