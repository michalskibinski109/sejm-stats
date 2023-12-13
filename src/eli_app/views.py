from django.views.generic import ListView
from eli_app.models import Act, Publisher, ActStatus, Keyword
import json
from django.db.models import Count


class ActListView(ListView):
    model = Act
    template_name = "act_list.html"
    context_object_name = "acts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publishers"] = Publisher.objects.all()
        context["keywords"] = Keyword.objects.all()
        context["statuses"] = ActStatus.objects.all().annotate(total=Count("act"))
        context["selected_statuses"] = self.request.GET.getlist("status")
        print(context["selected_statuses"])
        return context

    def get_queryset(self):
        queryset = Act.objects.order_by("-changeDate")
        publisher = self.request.GET.get("publisher")
        statuses = self.request.GET.getlist("status")
        minDate = self.request.GET.get("minDate")
        maxDate = self.request.GET.get("maxDate")
        if publisher:
            queryset = queryset.filter(publisher__name=publisher)
        if statuses:
            queryset = queryset.filter(status__name__in=statuses)
        if minDate:
            queryset = queryset.filter(changeDate__gte=minDate)
        if maxDate:
            queryset = queryset.filter(changeDate__lte=maxDate)

        return queryset[:500]
