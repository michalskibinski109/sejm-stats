from django.views.generic import DetailView
from sejm_app.models import Envoy, Voting, VotingOption
from sejm_app.libs.wikipedia_searcher import get_wikipedia_biography
from loguru import logger


class EnvoyDetailView(DetailView):
    model = Envoy
    template_name = "envoy_detail.html"  # replace with your template
    context_object_name = "envoy"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["interpellations"] = self.object.interpellations.all()
        logger.debug(f"Interpellations: {context['interpellations']}")
        context["biography"] = get_wikipedia_biography(self.object.title)
        context["latest_votings"] = self.get_latest_votings(5)
        return context

    def get_latest_votings(self, n):
        votes = self.object.votes
        logger.debug(f"Votes: {votes}")
        votings = (
            Voting.objects.filter(votes__in=votes.all())
            .distinct()
            .order_by("-date")[:n]
        )
        for voting in votings:
            text_vote = voting.votes.filter(MP=self.object).last().vote_label
            voting.envoy_vote = text_vote
        return votings
