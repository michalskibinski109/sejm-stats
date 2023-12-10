from django.urls import path
from .views import (
    EnvoyListView,
    EnvoyDetailView,
    ClubListView,
    ClubDetailView,
    HomeView,
    VotingListView,
    VotingDetailView,
    FAQListView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("envoys/", EnvoyListView.as_view(), name="envoys"),
    path("envoys/<int:pk>", EnvoyDetailView.as_view(), name="envoy_detail"),
    path("clubs/", ClubListView.as_view(), name="clubs"),
    path("clubs/<int:pk>", ClubDetailView.as_view(), name="club_detail"),
    path("votings/", VotingListView.as_view(), name="votings"),
    path("voting/<int:pk>", VotingDetailView.as_view(), name="voting_detail"),
    path("faq/", FAQListView.as_view(), name="faq"),
]
