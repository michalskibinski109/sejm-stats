from elasticsearch_dsl import Search
from django.conf import settings
from django.shortcuts import render
from django.views import View
from sejm_app.models import PrintModel, Process, Envoy, Interpellation, Reply, Club
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.db.models import Count
import json
from django.db.models.functions import (
    TruncWeek,
)  # or TruncDay, TruncWeek based on your need

# Full-text search across multiple fields using SearchVector


class SearchResultView(View):
    def get(self, request):
        interpolations_query = Q()
        processes_query = Q()
        prints_query = Q()
        envoys_query = Q()
        query = request.GET.get("search", "").strip()
        keywords = query.split()
        for keyword in keywords:
            interpolations_query |= Q(
                title__icontains=keyword
            )  # Add more fields if needed
            processes_query |= Q(title__icontains=keyword)  # Add more fields if needed
            prints_query |= Q(title__icontains=keyword)  # Add more fields if needed
            envoys_query |= Q(first_name__icontains=keyword) | Q(
                second_name__icontains=keyword
            )

        # Filter based on constructed Q objects
        interpolations = Interpellation.objects.filter(interpolations_query)
        processes = Process.objects.filter(processes_query)
        prints = PrintModel.objects.filter(prints_query)
        envoys = Envoy.objects.filter(envoys_query)

        context = {
            "query": query,
            "interpelations": interpolations,
            "processes": processes,
            "prints": prints,
            "envoys": envoys,
            "total": len(interpolations) + len(processes) + len(prints) + len(envoys),
            "commitment": self._get_envoys_commitment(interpolations),
            "topic_interest_over_time": json.dumps(
                self._get_topic_interest_over_time(interpolations, processes, prints)
            ),
            "number_of_projects_by_club": json.dumps(
                self._get_number_of_projects_by_club(processes)
            ),
        }

        return render(request, "query_results.html", context)

    def _get_number_of_projects_by_club(self, processes) -> dict:
        import random

        clubs = Club.objects.all()
        return {club.id: random.randint(0, 20) for club in clubs}

    def _get_topic_interest_over_time(self, interpolations, processes, prints) -> dict:
        # Aggregate interpellations by week
        interp_agg = (
            Interpellation.objects.filter(
                id__in=[interp.id for interp in interpolations]
            )
            .annotate(
                week=TruncWeek("receipt_date")
            )  # Assuming 'receipt_date' is the relevant date field
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Aggregate processes by week
        proc_agg = (
            Process.objects.filter(id__in=[proc.id for proc in processes])
            .annotate(week=TruncWeek("process_start_date"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Aggregate prints by week
        print_agg = (
            PrintModel.objects.filter(id__in=[printm.id for printm in prints])
            .annotate(week=TruncWeek("document_date"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Format and separate the results for each model
        return {
            "interpolations": {
                entry["week"].strftime("%Y-%m-%d"): entry["count"]
                for entry in interp_agg
            },
            "processes": {
                entry["week"].strftime("%Y-%m-%d"): entry["count"] for entry in proc_agg
            },
            "prints": {
                entry["week"].strftime("%Y-%m-%d"): entry["count"]
                for entry in print_agg
            },
        }

    def _get_envoys_commitment(self, interpelations: list[Interpellation]) -> dict:
        envoys = (
            Envoy.objects.filter(interpellations__in=interpelations)
            .annotate(num_interpellations=Count("interpellations"))
            .order_by("-num_interpellations")[:5]
        )

        envoys_commitment = {
            str(envoy): envoy.num_interpellations
            for envoy in envoys
            if envoy.num_interpellations > 0
        }
        return json.dumps(envoys_commitment)
