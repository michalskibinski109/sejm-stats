from django.db.models import F
from django.views.generic import TemplateView
from sejm_app.models import Voting, Scandal, Club, Process


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_votings"] = Voting.objects.order_by("-date")[:5]
        context["all_clubs"] = Club.objects.all().count()
        cards = [
            {
                "title": "Wszystkich głosowań",
                "count": Voting.objects.all().count(),
                "color": "",
            },
            {
                "title": "Wszystkich afer rządowych",
                "count": Scandal.objects.all().count(),
                "color": "text-danger",
            },
            {
                "title": "Wszystkich projektów",
                "count": Process.objects.all().count(),
                "color": "",
            },
            {
                "title": "Oczekujących projektów",
                "count": sum(
                    1 for process in Process.objects.all() if not process.is_finished
                ),
                "color": "",
            },
        ]
        context["cards"] = cards
        return context
