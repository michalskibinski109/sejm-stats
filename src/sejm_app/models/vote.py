from django.db import models
from django.utils.translation import gettext_lazy as _


class VotingOption(models.IntegerChoices):
    YES = 1, _("Yes")
    NO = 0, _("No")
    ABSTAIN = 2, _("ABSTAIN")
    ABSENT = 3, _("ABSENT")


class Vote(models.Model):
    voting = models.ForeignKey(
        "Voting", on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    MP = models.ForeignKey(
        "Envoy", on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    vote = models.SmallIntegerField(
        choices=VotingOption.choices,
        help_text=_("Vote option"),
    )
