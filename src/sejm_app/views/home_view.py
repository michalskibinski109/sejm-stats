from django.db.models import F
from django.views.generic import TemplateView
from sejm_app.models import Voting, Scandal, Club


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_votings"] = Voting.objects.all().count()
        context["passed_votings"] = Voting.objects.filter(yes__gt=F("no")).count()
        context["latest_votings"] = Voting.objects.order_by("-date")[:5]
        context["all_scandals"] = Scandal.objects.all().count()
        context["all_clubs"] = Club.objects.all().count()
        # context["scandals"] = Scandal.objects.order_by("-date")[:5]
        return context
