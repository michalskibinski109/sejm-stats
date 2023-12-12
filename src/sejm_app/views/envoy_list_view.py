from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from sejm_app.models import Envoy, Club


class EnvoyListView(ListView):
    model = Envoy
    template_name = "envoy_list.html"  # replace with your template
    context_object_name = "envoys"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clubs"] = Club.objects.all()
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            query_parts = query.strip().split()
            qf = Q()
            for part in query_parts:
                qf &= Q(first_name__icontains=part) | Q(last_name__icontains=part)

            return Envoy.objects.filter(qf).order_by("first_name", "last_name")
        return super().get_queryset()

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html = render_to_string(
                "_envoy_snippet.html", context, request=self.request
            )
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)
