# import django settings
from django.conf import settings
import requests
from sejm_app.models import (
    Club,
    Envoy,
    Vote,
    Voting,
    Interpellation,
    VotingOption,
    PrintModel,
    AdditionalPrint,
    Process,
)
from sejm_app.libs.wikipedia_searcher import get_wikipedia_biography

from loguru import logger
from django.db.utils import OperationalError
import io
from django.core.files.base import ContentFile
import urllib.parse as urlparse
from django.utils import timezone
from datetime import datetime
from django.db import ProgrammingError, models

# import infinite number itereator
from itertools import count

# select * from sys.objects
# order by modify_date desc


def run():
    try:
        Club.objects.first()
        Voting.objects.first()
    except (OperationalError, ProgrammingError):
        logger.info("Database not initialized yet")
        return
    # download_clubs()
    # download_envoys()
    # download_photos()
    # download_clubs_photos()
    # download_votings()
    # download_prints()
    # download_processes()
    # download_interpellations()


def download_processes():
    url = f"{settings.SEJM_ROOT_URL}/processes"
    last_process = (
        int(Process.objects.order_by("number").last().number) + 1
        if Process.objects.exists()
        else 1
    )
    MAX_MISSING = 8
    missing = 0
    logger.info(f" last num {last_process} ")
    for i in count(last_process):
        logger.info(f"Downloading process {i}")
        if f"{settings.TERM}{i}" in Process.objects.values_list("id", flat=True):
            continue
        resp = requests.get(f"{url}/{i}")
        if missing > MAX_MISSING:
            logger.info(f"Finished downloading processes on {i}")
            return
        if resp.status_code != 200:
            missing += 1
            logger.info(f"Missing process {i} ({missing}/{MAX_MISSING})")
            continue
        else:
            missing = 0
            process = resp.json()
            process = Process.from_api_response(process)
            logger.info(f"Downloaded process {process.id}")


def download_prints():
    url = f"{settings.SEJM_ROOT_URL}/prints"
    logger.info(f"Downloading prints from {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    prints = resp.json()
    print(f"Downloaded {len(prints)} prints")
    for print_ in prints[::-1]:
        if PrintModel.objects.filter(id=f'{print_["term"]}{print_["number"]}').exists():
            break
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
