from django.views.generic import DetailView
from sejm_app.models import Envoy, Voting, VotingOption, ClubVote
from loguru import logger
import json

# import defaultdict
from collections import defaultdict


class EnvoyDetailView(DetailView):
    model = Envoy
    template_name = "envoy_detail.html"  # replace with your template
    context_object_name = "envoy"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["interpellations"] = self.object.interpellations.all()
        logger.debug(f"Interpellations: {context['interpellations']}")
        context["latest_votings"] = self.get_latest_votings(5)
        context["discipline_ratio"] = self.get_discipline_ratio()
        return context

    def get_latest_votings(self, n):
        votes = self.object.votes.all()
        logger.debug(f"Votes: {votes}")
        votings = (
            Voting.objects.filter(votes__in=votes).distinct().order_by("-date")[:n]
        )
        for voting in votings:
            text_vote = voting.votes.filter(MP=self.object).last().vote_label
            voting.envoy_vote = text_vote
        return votings

    def get_discipline_ratio(self):
        votes = self.object.votes.all()
        votings = Voting.objects.filter(votes__in=votes).distinct().order_by("-date")
        club = self.object.club
        voting_dict = defaultdict(int)
        for voting in votings:
            try:
                club_vote = voting.club_votes.get(club=club)
            except ClubVote.MultipleObjectsReturned:
                logger.warning(f"Club vote for {voting.club_votes.filter(club=club)}")

                continue
            most_popular = (
                VotingOption.NO if club_vote.no > club_vote.yes else VotingOption.YES
            )
            envoy_vote = self.object.votes.get(voting=voting).vote
            if envoy_vote in [
                VotingOption.ABSENT,
                VotingOption.VOTE_VALID,
                VotingOption.ABSTAIN,
            ]:
                voting_dict["brak głosu"] += 1
            elif most_popular == envoy_vote:
                voting_dict["zgodnie"] += 1
            else:
                voting_dict["nie zgodnie"] += 1
                logger.warning(f"envoy vote: {envoy_vote}, club vote: {club_vote}")

        return json.dumps(voting_dict)
