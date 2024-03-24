from django.views.generic import ListView
from sejm_app.forms import CommitteeSearchForm
from sejm_app.models import Committee


class CommitteeListView(ListView):
    model = Committee
    template_name = "committee_list.html"
    context_object_name = "committees"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CommitteeSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["type"]:
                queryset = queryset.filter(type=form.cleaned_data["type"])
            if form.cleaned_data["appointmentDate_from"]:
                queryset = queryset.filter(
                    appointmentDate__gte=form.cleaned_data["appointmentDate_from"]
                )
            if form.cleaned_data["appointmentDate_to"]:
                queryset = queryset.filter(
                    appointmentDate__lte=form.cleaned_data["appointmentDate_to"]
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommitteeSearchForm(self.request.GET)
        return context
