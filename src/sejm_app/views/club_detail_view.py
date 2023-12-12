from sejm_app.models import Club, Envoy


from django.views.generic import DetailView


class ClubDetailView(DetailView):
    model = Club
    template_name = "club_detail.html"  # replace with your template
    context_object_name = "club"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["envoys"] = Envoy.objects.filter(club=context["club"])
    #     return context
