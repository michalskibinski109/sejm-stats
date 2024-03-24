from django.conf import settings
from loguru import logger
import requests
from sejm_app import models
from django.db.models import Model

from sejm_app.libs.wikipedia_searcher import get_wikipedia_biography
from sejm_app.models.club import Club
from sejm_app.models.print_model import AdditionalPrint, PrintModel
from sejm_app.utils import parse_all_dates
from .db_updater_task import DbUpdaterTask
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction


class PrintsUpdaterTask(DbUpdaterTask):
    # DEPENDS ON ClubUpdaterTask
    MODEL: Model = models.PrintModel
    DATE_FIELD_NAME = "documentDate"

    def run(self, *args, **kwargs):
        logger.info("Updating prints")
        self._download_prints()

    def _create_print(self, print_):
        logger.info(f"Creating print {print_['number']}")
        print_ = parse_all_dates(print_)
        print_.pop("attachments")
        add_prints = []
        print_.pop("processPrint")
        if print_.get("additionalPrints"):
            add_prints = print_.pop("additionalPrints")
        print_mdl = PrintModel.objects.create(**print_)
        for add_print in add_prints:
            if add_print.get("processPrint"):
                add_print.pop("processPrint")
            add_print.pop("attachments")
            add_print.pop("numberAssociated")
            add_print["main_print"] = print_mdl
            AdditionalPrint.objects.create(**add_print)

    def _download_prints(self):
        url = f"{settings.SEJM_ROOT_URL}/prints"
        logger.info(f"Downloading prints from {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        prints = resp.json()
        print(f"Downloaded {len(prints)} prints")
        for print_ in prints[::-1]:
            if PrintModel.objects.filter(number=print_["number"]).exists():
                break
            with transaction.atomic():
                self._create_print(print_)
        logger.info("Finished updating prints")
