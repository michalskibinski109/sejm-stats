from __future__ import annotations
from django.db import models
from django.utils.translation import gettext_lazy as _


class Club(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    members_count = models.IntegerField()
    photo = models.ImageField(upload_to="photos", null=True, blank=True)


class Envoy(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="photos", null=True, blank=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    active = models.BooleanField(default=True)
    inactive_cause = models.CharField(max_length=255, null=True, blank=True)
    waiver_desc = models.TextField(null=True, blank=True)
    district_num = models.IntegerField()
    district_name = models.CharField(max_length=255)
    voivodeship = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="envoys")
    birth_date = models.DateField()
    birth_location = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    number_of_votes = models.IntegerField()


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


class VotingOption(models.IntegerChoices):
    YES = 1, _("Yes")
    NO = 0, _("No")
    ABSTAIN = 2, _("ABSTAIN")
    ABSENT = 3, _("ABSENT")


class Vote(models.Model):
    voting = models.ForeignKey(
        Voting, on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    MP = models.ForeignKey(Envoy, on_delete=models.CASCADE, null=True, blank=True)
    vote = models.SmallIntegerField(
        choices=VotingOption.choices,
        help_text=_("Vote option"),
    )
