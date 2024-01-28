from elasticsearch_dsl import Search
from django.conf import settings
from django.shortcuts import render
from django.views import View
from sejm_app.models import PrintModel, Process, Envoy, Interpellation
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

# Full-text search across multiple fields using SearchVector


class SearchResultView(View):
    def get(self, request):
        interpelations_query = Q()
        processes_query = Q()
        prints_query = Q()
        envoys_query = Q()
        query = request.GET.get("search", "").strip()
        keywords = query.split()
        for keyword in keywords:
            interpelations_query |= Q(
                title__icontains=keyword
            )  # Add more fields if needed
            processes_query |= Q(title__icontains=keyword)  # Add more fields if needed
            prints_query |= Q(title__icontains=keyword)  # Add more fields if needed
            envoys_query |= Q(first_name__icontains=keyword) | Q(
                second_name__icontains=keyword
            )

        # Filter based on constructed Q objects
        interpelations = Interpellation.objects.filter(interpelations_query)
        processes = Process.objects.filter(processes_query)
        prints = PrintModel.objects.filter(prints_query)
        envoys = Envoy.objects.filter(envoys_query)

        context = {
            "query": query,
            "interpelations": interpelations,
            "processes": processes,
            "prints": prints,
            "envoys": envoys,
            "total": len(interpelations) + len(processes) + len(prints) + len(envoys),
        }

        return render(request, "query_results.html", context)
