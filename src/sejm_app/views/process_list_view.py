from sejm_app.models import Process, Stage
from django.views.generic import ListView
from django.db.models import Count
from sejm_app.forms import ProcessSearchForm


class ProcessListView(ListView):
    model = Process
    template_name = "process_list.html"
    context_object_name = "processes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProcessSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .annotate(stage_count=Count("stages"))
            .filter(stage_count__gt=1)
        )
        form = ProcessSearchForm(self.request.GET)
        if form.is_valid():
            document_types = form.cleaned_data.get("document_type")
            if document_types:
                queryset = queryset.filter(document_type__in=document_types)
        return queryset
