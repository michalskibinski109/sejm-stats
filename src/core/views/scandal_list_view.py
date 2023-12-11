from core.models import Scandal


from django.views.generic import ListView


class ScandalListView(ListView):
    model = Scandal
    template_name = "scandal_list.html"  # replace with your template
    context_object_name = "scandals"
