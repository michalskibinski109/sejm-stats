from django.db.models import Count
from django.views.generic import ListView
from sejm_app.models import Club

import json


class ClubListView(ListView):
    model = Club
    template_name = "club_list.html"  # replace with your template
    context_object_name = "clubs"

    def get_queryset(self):
        # Annotate each club with the count of its envoys and order by this count
        return Club.objects.order_by("-membersCount")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs_list = [
            {"id": club.id, "envoys_count": club.membersCount}
            for club in context["clubs"]
        ]
        context["clubs_json"] = json.dumps(clubs_list)
        return context
