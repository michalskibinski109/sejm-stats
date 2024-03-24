from itertools import count
from django.db import transaction
from loguru import logger
import requests
from django.conf import settings
from sejm_app.models import Process, Stage, Voting, Envoy, Club
from sejm_app.models.print_model import PrintModel
from sejm_app.models.process import CreatedByEnum
from sejm_app.utils import parse_all_dates
from .db_updater_task import DbUpdaterTask
from django.utils.timezone import make_aware

from typing import Optional, Dict, Any
from eli_app.libs.pdf_parser import (
    get_pdf_authors,
)  # Ensure this import is corrected based on your actual module structure
from django.db.models import Max


class ProcessesUpdaterTask(DbUpdaterTask):
    MODEL: Any = Process
    DATE_FIELD_NAME: str = "changeDate"
    MAX_MISSING: int = 8

    def run(self, *args, **kwargs):
        logger.info("Updating processes")
        self._download_processes()

    def _download_processes(self) -> None:
        base_url: str = f"{settings.SEJM_ROOT_URL}/processes"
        last_number: int = (
            Process.objects.aggregate(max_number=Max("number"))["max_number"] or 0
        )
        missing_count: int = 0
        for number in count(start=last_number + 1):
            if missing_count > self.MAX_MISSING:
                logger.info(f"Finished downloading processes {number - 1}")
                break
            if process_data := self._fetch_process(base_url, number):
                missing_count = 0
                with transaction.atomic():
                    self._create_or_update_process(process_data)
            else:
                missing_count += 1
                continue

    def _fetch_process(self, url: str, number: int) -> dict | None:
        response = requests.get(f"{url}/{number}")
        if response.status_code != 200:
            logger.info(f"Missing process {number}")
            return None
        return parse_all_dates(response.json(), date_only=True)

    def _create_or_update_process(self, data: dict) -> None:
        process_id: str = f"{data['term']}{data['number']}"
        if "UE" in data:
            data["UE"] = True if data["UE"] == "YES" else False
        data["createdBy"] = self._get_type_of_process(
            data["title"], data["documentType"]
        )
        try:
            data["printModel"] = PrintModel.objects.get(
                term=data["term"], number=data["number"]
            )
        except PrintModel.DoesNotExist:
            data["printModel"] = None
        data.pop("printsConsideredJointly", None)
        data.pop("otherDocuments", None)
        stages_data = data.pop("stages", [])
        process, created = Process.objects.update_or_create(
            id=process_id, defaults=data
        )
        if created:
            logger.debug(f"Created process {process_id} created by {process.createdBy}")
            self._assign_authors(process, data)
            # if key == "print_model":
        for stage in stages_data:
            self._create_or_update_stage(stage, process)

    def _create_or_update_stage(self, data: dict, process):
        stage = Stage()
        if len(data.get("children", ())) != 1:
            logger.debug(
                f"{len(data.get('children', ()))} children for stage in {process.id}"
            )
            return
        child = data.pop("children")[0]
        for key in data.keys():
            if key in child:
                del child[key]
        data.update(child)
        data = parse_all_dates(data)
        for key, value in data.items():
            if key == "voting" and value:
                stage.voting = self._get_voting(value)
                continue
            if not hasattr(stage, key):
                continue
            setattr(stage, key, value)
        process.save()
        stage.process = process
        stage.save()
        return stage

    def _get_voting(self, voting_data: Dict[str, Any]) -> None:
        return Voting.objects.filter(
            date=voting_data["date"],
            votingNumber=voting_data["votingNumber"],
        ).first()

    def _assign_authors(self, process: Process, data: Dict[str, Any]) -> None:
        if process.createdBy == CreatedByEnum.CLUB:
            for club in Club.objects.all():
                if club.name.lower() in process.title.lower():
                    process.club = club
                    process.save()
                    return
        elif process.createdBy == CreatedByEnum.ENVOYS:
            envoys = Envoy.objects.all()
            possible_authors = get_pdf_authors(
                process.printModel.pdf_url
            )  # Adjust this based on actual PDF URL source
            for author in possible_authors:
                first_name, last_name = author.split(" ")[0], author.split(" ")[-1]
                if envoy := envoys.filter(
                    firstName__iexact=first_name, lastName__iexact=last_name
                ).first():
                    process.MPs.add(envoy)

    def _get_type_of_process(self, title: str, documentType: str) -> str:
        if documentType.lower() not in [
            "projekt ustawy",
            "wniosek",
            "projekt uchwały",
        ]:
            return ""
        if title.lower().startswith("poselski"):
            return CreatedByEnum.ENVOYS
        if "prezydium sejmu" in title.lower():
            return CreatedByEnum.PRESIDIUM
        if "obywatelski" in title.lower():
            return CreatedByEnum.CITIZENS
        if "rządowy" in title.lower():
            return CreatedByEnum.GOVERNMENT
        if "przez klub parlamentarny" in title.lower():
            return CreatedByEnum.CLUB
        return ""
