from sejm_app.models import Process, Stage
from django.views.generic import ListView
from django.db.models import Count


class ProcessListView(ListView):
    model = Process
    template_name = "process_list.html"
    context_object_name = "processes"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(stage_count=Count("stages"))
            .filter(stage_count__gt=1)
        )
