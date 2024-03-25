from celery import current_app
from django.conf import settings
import requests
from sejm_app.db_updater.db_updater_task import DbUpdaterTask
from sejm_app.models import Committee, Envoy, CommitteeMember, Club
from django.utils.dateparse import parse_date
from loguru import logger
from django.db import transaction


class CommitteeUpdaterTask(DbUpdaterTask):
    MODEL = Committee
    DATE_FIELD_NAME = "appointmentDate"

    def run(self, *args, **kwargs):
        response = requests.get(f"{settings.SEJM_ROOT_URL}/committees")
        if response.status_code == 200:
            committees_data = response.json()
            for committee_data in committees_data:
                with transaction.atomic():
                    self.update_or_create_committee(committee_data)

    def update_or_create_committee(self, data):
        committee, _ = Committee.objects.update_or_create(
            id=data["code"],
            defaults={
                "name": data["name"],
                "nameGenitive": data["nameGenitive"],
                "appointmentDate": parse_date(data["appointmentDate"]),
                "compositionDate": parse_date(data["compositionDate"]),
                "phone": data.get("phone", ""),
                "scope": data.get("scope"),
                "type": data["type"],
            },
        )
        self._update_or_create_members(committee, data.get("members", []))

    def _update_or_create_members(self, committee, members):
        for member_data in members:
            envoy = Envoy.objects.get(id=member_data["id"])
            CommitteeMember.objects.update_or_create(
                committee=committee,
                envoy=envoy,
                defaults={
                    "function": member_data.get("function"),
                },
            )
