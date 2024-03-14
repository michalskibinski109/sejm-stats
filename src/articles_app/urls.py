from django.urls import path
from .views import ArticleListView, ArticleDetailView

name = "articles"
urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
    path(
        "article-detail/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"
    ),
]
