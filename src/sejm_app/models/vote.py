from django.db import models
from django.utils.translation import gettext_lazy as _
from sejm_app.models.envoy import Envoy
from sejm_app.utils import camel_to_snake, parse_all_dates


class VotingOption(models.IntegerChoices):
    NO = 0, _("No")
    YES = 1, _("Yes")
    ABSTAIN = 2, _("ABSTAIN")
    ABSENT = 3, _("ABSENT")
    VOTE_VALID = 4, _("VOTE_VALID")


class Vote(models.Model):
    id = models.IntegerField(primary_key=True)
    voting = models.ForeignKey("Voting", on_delete=models.CASCADE, related_name="votes")
    MP = models.ForeignKey("Envoy", on_delete=models.CASCADE, related_name="votes")
    vote = models.SmallIntegerField(
        choices=VotingOption.choices,
        help_text=_("Vote option"),
    )

    def save(self, *args, **kwargs):
        self.id = self.voting.pk * 1000 + self.MP.pk
        super().save(*args, **kwargs)

    @property
    def vote_label(self):
        dct = {
            VotingOption.NO: "Przeciw",
            VotingOption.YES: "Za",
            VotingOption.ABSTAIN: "Wstzymanie się",
            VotingOption.ABSENT: "Nieobecność",
            VotingOption.VOTE_VALID: "Głos ważny",
        }
        return dct[self.vote]


class ClubVote(models.Model):

    club = models.ForeignKey(
        "Club", on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    yes = models.IntegerField(default=0)
    no = models.IntegerField(default=0)
    abstain = models.IntegerField(default=0)
    voting = models.ForeignKey(
        "Voting",
        on_delete=models.CASCADE,
        related_name="club_votes",
    )
