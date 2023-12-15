from django.views.generic import ListView
from eli_app.models import Act, Publisher, ActStatus, Keyword
from .forms import SearchForm
import json
from django.db.models import Count
from loguru import logger


class ActListView(ListView):
    model = Act
    template_name = "act_list.html"
    context_object_name = "acts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        queryset = Act.objects.order_by("-changeDate")
        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            keywords = form.cleaned_data.get("keywords")
            if keywords and not isinstance(keywords, list):
                keywords = [keywords]
            publisher = form.cleaned_data.get("publisher")
            status = form.cleaned_data.get("status")
            minDate = form.cleaned_data.get("minDate")
            maxDate = form.cleaned_data.get("maxDate")
            if keywords:
                queryset = queryset.filter(keywords__in=keywords)
            if publisher:
                queryset = queryset.filter(publisher=publisher)
            if status:
                queryset = queryset.filter(status=status)
            if minDate:
                queryset = queryset.filter(changeDate__gte=minDate)
            if maxDate:
                queryset = queryset.filter(changeDate__lte=maxDate)

        return queryset[:250]
