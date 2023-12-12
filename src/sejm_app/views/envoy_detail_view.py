from django.views.generic import DetailView
from sejm_app.models import Envoy


class EnvoyDetailView(DetailView):
    model = Envoy
    template_name = "envoy_detail.html"  # replace with your template
    context_object_name = "envoy"
