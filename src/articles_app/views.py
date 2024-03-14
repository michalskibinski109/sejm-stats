from django.views.generic import ListView
from articles_app.models import Article
import json
from django.db.models import Count
from loguru import logger


class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"


class ArticleDetailView(ListView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = Article.objects.get(pk=self.kwargs["pk"])
        return context
