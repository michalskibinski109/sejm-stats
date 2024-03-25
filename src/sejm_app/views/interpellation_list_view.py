from django.views.generic import ListView
from sejm_app.models import Interpellation


class InterpellationListView(ListView):
    model = Interpellation
    template_name = "interpellation_list.html"  # Path to the template
    context_object_name = "interpellations"
