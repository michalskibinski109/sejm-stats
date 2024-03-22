from elasticsearch_dsl import Search
from django.conf import settings
from django.shortcuts import render
from django.views import View
from sejm_app.models import PrintModel, Process, Envoy, Interpellation, Reply, Club
from eli_app.models import Act
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.db.models import Count
import json
from django.db.models.functions import (
    TruncWeek,
)  # or TruncDay, TruncWeek based on your need
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from django.db.models.functions import Greatest
from loguru import logger

# Full-text search across multiple fields using SearchVector


class SearchResultView(View):
    def get(self, request):
        query = request.GET.get("search", "").strip()
        logger.debug(f"Query: {query}")
        keywords = query.split(",")
        search_queries = [
            SearchQuery(keyword.strip(), config="pl_ispell") for keyword in keywords
        ]
        combined_search_query = search_queries.pop()
        for search_query in search_queries:
            combined_search_query |= search_query
        title_vector = SearchVector("title", config="pl_ispell")
        keyword_vector = SearchVector("keywords", config="pl_ispell")
        person_vector = SearchVector(
            "firstName", "secondName", "lastName", config="pl_ispell"
        )
        interpolations = (
            Interpellation.objects.annotate(
                search=title_vector,
            )
            .filter(search=combined_search_query)
            .order_by("-last_modified")
        )
        processes = Process.objects.annotate(search=title_vector).filter(
            search=combined_search_query
        )
        prints = PrintModel.objects.annotate(search=title_vector).filter(
            search=combined_search_query
        )
        envoys = Envoy.objects.annotate(search=person_vector).filter(
            search=combined_search_query
        )
        # use title and keyword vector
        acts = (
            Act.objects.annotate(search=title_vector + keyword_vector)
            .filter(search=combined_search_query)
            .order_by("-announcementDate")
        )
        logger.debug(f"Found models.")
        context = {
            "query": query.split(","),
            "acts": acts,  # TODO only temporary
            "interpellations": interpolations,
            "processes": processes,
            "prints": prints,
            "envoys": envoys,
            "total": len(interpolations)
            + len(processes)
            + len(prints)
            + len(envoys)
            + len(acts),
            "commitment": self._get_envoys_commitment(interpolations),
            "topic_interest_over_time": json.dumps(
                self._get_topic_interest_over_time(interpolations, processes, prints)
            ),
            "clubs_involvement": json.dumps(
                self._get_clubs_involvement(interpolations)
            ),
        }
        logger.debug(f"running render.")

        return render(request, "query_results.html", context)

    def _get_clubs_involvement(
        self,
        interpolations: list[Interpellation],
    ) -> dict:

        return {
            club.id: interpolations.filter(from_member__club=club).count()
            for club in Club.objects.all()
        }

    def _get_topic_interest_over_time(self, interpolations, processes, prints) -> dict:
        # Aggregate interpellations by week
        interp_agg = (
            Interpellation.objects.filter(
                id__in=interpolations.values_list("id", flat=True)
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
            Process.objects.filter(id__in=processes.values_list("id", flat=True))
            .annotate(week=TruncWeek("process_start_date"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Aggregate prints by week
        print_agg = (
            PrintModel.objects.filter(id__in=prints.values_list("id", flat=True))
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
