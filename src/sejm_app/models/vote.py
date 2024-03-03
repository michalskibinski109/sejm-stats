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

    @classmethod
    def from_api_response(cls, response: dict, voting: "Voting"):
        # https://api.sejm.gov.pl/sejm/openapi/ui/#/default/get_sejm_term_term__votings__sitting___num_
        vote = cls()
        vote.voting = voting
        response = {camel_to_snake(key): value for key, value in response.items()}
        response = parse_all_dates(response)
        for key, value in response.items():
            if not hasattr(vote, key):
                continue
            if key == "MP":
                value = Envoy.objects.get(id=value)
            if key == "vote":
                value = VotingOption[value.upper()].value
            setattr(vote, key, value)
        if voting.votes.filter(MP=vote.MP).exists():
            return voting.votes.get(MP=vote.MP)
        vote.save()
        return vote


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
