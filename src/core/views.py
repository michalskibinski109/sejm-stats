from django.db.models import Prefetch
from django.http import JsonResponse
from django.db.models import Q, Count, F
import json

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView
from .models import Club, Envoy, Voting, Scandal, FAQ

from django.template.loader import render_to_string


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_votings"] = Voting.objects.all().count()
        context["passed_votings"] = Voting.objects.filter(yes__gt=F("no")).count()
        context["latest_votings"] = Voting.objects.order_by("-date")[:5]
        context["all_scandals"] = Scandal.objects.all().count()
        context["all_clubs"] = Club.objects.all().count()
        # context["scandals"] = Scandal.objects.order_by("-date")[:5]
        return context


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


class EnvoyDetailView(DetailView):
    model = Envoy
    template_name = "envoy_detail.html"  # replace with your template
    context_object_name = "envoy"


class ClubListView(ListView):
    model = Club
    template_name = "club_list.html"  # replace with your template
    context_object_name = "clubs"

    def get_queryset(self):
        # Annotate each club with the count of its envoys and order by this count
        return Club.objects.annotate(envoys_count=Count("envoys")).order_by(
            "-envoys_count"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs_list = [
            {"id": club.id, "envoys_count": club.envoys_count}
            for club in context["clubs"]
        ]
        context["clubs_json"] = json.dumps(clubs_list)
        return context


class ClubDetailView(DetailView):
    model = Club
    template_name = "club_detail.html"  # replace with your template
    context_object_name = "club"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["envoys"] = Envoy.objects.filter(club=context["club"])
        return context


class VotingListView(ListView):
    model = Voting
    template_name = "voting_list.html"  # replace with your template
    context_object_name = "votings"


class VotingDetailView(DetailView):
    model = Voting
    template_name = "voting_detail.html"  # replace with your template
    context_object_name = "voting"


class FAQListView(ListView):
    model = FAQ
    template_name = "faq_list.html"  # replace with your template
    context_object_name = "faqs"
