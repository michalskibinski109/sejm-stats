from django.db.models import F
from django.urls import reverse
from django.views.generic import TemplateView
from sejm_app.models import Voting, Scandal, Club, Process
from loguru import logger


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
                "url": reverse("votings"),
            },
            {
                "title": "Wszystkich afer rządowych",
                "count": Scandal.objects.all().count(),
                "color": "text-danger",
                "url": reverse("scandals"),
            },
            {
                "title": "Wszystkich projektów",
                "count": Process.objects.all().count(),
                "color": "",
                "url": reverse("processes"),
            },
            {
                "title": "Oczekujących projektów",
                "count": sum(
                    not process.is_finished for process in Process.objects.all()
                ),
                "color": "",
                # http://127.0.0.1:8000/processes/?state=on
                "url": reverse("processes") + "?state=on",
            },
        ]
        context["cards"] = cards
        return context
