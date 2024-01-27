from elasticsearch_dsl import Search
from django.conf import settings
from django.shortcuts import render
from django.views import View


class SearchResultView(View):
    def get(self, request):
        query = request.GET.get("query", "")

        # s = Search(
        #     using=settings.ELASTICSEARCH_DSL["default"]["hosts"],
        #     index="print,process,envoy",
        # )
        # s = s.query("multi_match", query=query, fields=["*"])

        # response = s.execute()

        # results = [hit.to_dict() for hit in response]
        results = []
        context = {
            "query": query,
            "results": results,
        }

        return render(request, "query_results.html", context)
