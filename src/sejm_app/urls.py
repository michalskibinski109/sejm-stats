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
    ScandalListView,
    ProcessListView,
    ProcessDetailView,
    SearchResultView,
    UpdateView,
    LastUpdateView,
    CommitteeListView,
    CommitteeDetailView,
    InterpellationDetailView,
    InterpellationListView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("last-update/", LastUpdateView.as_view(), name="last_update"),
    path("search/", SearchResultView.as_view(), name="search"),
    path("envoys/", EnvoyListView.as_view(), name="envoys"),
    path("envoys/<int:pk>", EnvoyDetailView.as_view(), name="envoy_detail"),
    path("clubs/", ClubListView.as_view(), name="clubs"),
    path("clubs/<str:pk>/", ClubDetailView.as_view(), name="club_detail"),
    path("votings/", VotingListView.as_view(), name="votings"),
    path("voting/<int:pk>/", VotingDetailView.as_view(), name="voting_detail"),
    path("faq/", FAQListView.as_view(), name="faq"),
    path("committees/", CommitteeListView.as_view(), name="committees"),
    path("committee/<str:pk>/", CommitteeDetailView.as_view(), name="committee_detail"),
    path("scandals/", ScandalListView.as_view(), name="scandals"),
    path("processes/", ProcessListView.as_view(), name="processes"),
    path("update/", UpdateView.as_view(), name="update"),
    path("process/<int:pk>/", ProcessDetailView.as_view(), name="process_detail"),
    path("interpellations/", InterpellationListView.as_view(), name="interpellations"),
    path(
        "interpellations/<int:pk>/",
        InterpellationDetailView.as_view(),
        name="interpellation_detail",
    ),
]
