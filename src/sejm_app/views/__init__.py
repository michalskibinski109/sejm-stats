from .process_detail_view import ProcessDetailView
from .process_list_view import ProcessListView
from .club_detail_view import ClubDetailView
from .club_list_view import ClubListView
from .envoy_detail_view import EnvoyDetailView
from .envoy_list_view import EnvoyListView
from .voting_detail_view import VotingDetailView
from .voting_list_view import VotingListView
from .home_view import HomeView
from .faq_list_view import FAQListView
from .scandal_list_view import ScandalListView
from .query_result_view import SearchResultView

from django.views.generic import View
from django.http import HttpResponse
from celery import chain


class UpdateView(View):

    def get(self, request):
        from sejm_app.tasks import tasks

        chain(t.s() for t in tasks).delay()
        return HttpResponse("Task initiated.")
