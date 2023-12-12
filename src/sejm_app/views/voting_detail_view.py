from sejm_app.models import Voting


from django.views.generic import DetailView


class VotingDetailView(DetailView):
    model = Voting
    template_name = "voting_detail.html"  # replace with your template
    context_object_name = "voting"
