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
            # .filter(stage_count__gt=1)
        )
        form = ProcessSearchForm(self.request.GET)
        if form.is_valid():
            documentTypes = form.cleaned_data.get("documentType")
            only_not_finished = form.cleaned_data.get("state")
            if documentTypes:
                queryset = queryset.filter(documentType__in=documentTypes)
            if only_not_finished:
                queryset = [
                    process for process in queryset if process.is_finished is False
                ]
        return queryset
