from django.views.generic import DetailView
from sejm_app.models import Process, Stage


class ProcessDetailView(DetailView):
    model = Process
    template_name = "process_detail.html"
    context_object_name = "process"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stages"] = self.object.stages.all().order_by("stageNumber")
        # get all distinct stage.decision
        return context
