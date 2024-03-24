from sejm_app.models import Committee


from django.views.generic import DetailView


class CommitteeDetailView(DetailView):
    model = Committee
    template_name = "committee_detail.html"  # replace with your template
    context_object_name = "committee"
