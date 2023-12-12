from sejm_app.models import Voting


from django.views.generic import ListView


class VotingListView(ListView):
    model = Voting
    template_name = "voting_list.html"  # replace with your template
    context_object_name = "votings"
