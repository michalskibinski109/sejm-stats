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
from django.db import models

# import infinite number itereator
from itertools import count

# select * from sys.objects
# order by modify_date desc


def camel_to_snake(name):
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def should_be_updated(model: models.Model, date_field: str):
    try:
        model.objects.first()

    except OperationalError:
        logger.info("Database not initialized yet")
        return False
    return not model.objects.order_by("-" + date_field).first() == timezone.now().date()


def run():
    try:
        Club.objects.first()
        Voting.objects.first()
    except OperationalError:
        logger.info("Database not initialized yet")
        return
    # download_clubs()
    # download_envoys()
    # download_photos()
    # download_clubs_photos()
    download_votings()

    # download_processes()
    # download_prints()
    # download_interpellations()


def download_interpellations():
    url = f"{settings.SEJM_ROOT_URL}/interpellations"
    last_interpellation = (
        Interpellation.objects.order_by("num").last().num
        if Interpellation.objects.exists()
        else 1
    )
    for i in count(last_interpellation):
        logger.info(f"Downloading interpellation {i}")
        if f"{settings.TERM}{i}" in Interpellation.objects.values_list("id", flat=True):
            continue
        resp = requests.get(f"{url}/{i}")
        if resp.status_code != 200:
            logger.info(f"Finished downloading interpellations on {i}")
            return
        else:
            interpellation = resp.json()
            interpellation = Interpellation.from_api_response(interpellation)


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
    if not should_be_updated(PrintModel, "change_date"):
        return
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
        print_ = {camel_to_snake(k): v for k, v in print_.items()}
        print_mdl = PrintModel.objects.create(**print_)
        for add_print in add_prints:
            if add_print.get("processPrint"):
                add_print.pop("processPrint")
            add_print.pop("attachments")
            add_print.pop("numberAssociated")
            add_print = {camel_to_snake(k): v for k, v in add_print.items()}
            add_print["main_print"] = print_mdl
            AdditionalPrint.objects.create(**add_print)


def download_envoys():
    if not Envoy.objects.exists():
        logger.info(f"Envoys don't exist in database. Calling {settings.ENVOYS_URL}")
        envoys = requests.get(settings.ENVOYS_URL).json()
        for envoy in envoys:
            envoy = {camel_to_snake(k): v for k, v in envoy.items()}
            # first_last_name,last_first_name // remove this fields

            envoy.pop("first_last_name")
            envoy.pop("last_first_name")
            envoy["club"] = Club.objects.get(id=envoy["club"])
            envoy = Envoy.objects.create(**envoy)
            download_biography(envoy)
    else:
        logger.info("Envoys already exists in database")


def download_biography(envoy: Envoy):
    biography, source = get_wikipedia_biography(envoy.title, with_source=True)
    envoy.biography = biography
    envoy.biography_source = source
    envoy.save()


def download_clubs():
    if not Club.objects.exists():
        logger.info(f"Clubs don't exist in database. Calling {settings.CLUBS_URL}")
        clubs = requests.get(settings.CLUBS_URL).json()
        for club in clubs:
            club_snake_case = {camel_to_snake(k): v for k, v in club.items()}
            Club.objects.create(**club_snake_case)
    else:
        logger.info("Clubs already exists in database")


def download_clubs_photos():
    # if not Club.objects.get(id=1).photo:
    logger.info("Downloading clubs photos")
    for club in Club.objects.all():
        if club.photo:
            continue
        photo_url = f"{settings.CLUBS_URL}/{club.id}/logo"
        photo = requests.get(photo_url)
        logger.info(f"Downloading photo for {club.id}")
        if photo.status_code == 200:
            photo_file = ContentFile(photo.content)
            club.photo.save(f"{club.id}.jpg", photo_file)
            club.save()
        else:
            logger.warning(f"Photo for {club.id} not found")


def download_photos():
    if not Envoy.objects.get(id=1).photo:
        logger.info("Downloading photos")
        for envoy in Envoy.objects.all():
            if envoy.photo:
                continue
            photo_url = f"{settings.ENVOYS_URL}/{envoy.id}/photo"
            photo = requests.get(photo_url)
            logger.info(f"Downloading photo for {envoy.id}")
            if photo.status_code == 200:
                photo_file = ContentFile(photo.content)
                envoy.photo.save(f"{envoy.id}.jpg", photo_file)
                envoy.save()
            else:
                logger.warning(f"Photo for {envoy.id} not found")


def download_votings():
    last_voting = (
        Voting.objects.order_by("-date").first() if Voting.objects.exists() else None
    )
    # check if last voting is from today
    if last_voting and last_voting.date.date() == timezone.now().date():
        logger.info("Votings are up to date")
        return
    sitting, number = (
        (last_voting.sitting, last_voting.voting_number + 1) if last_voting else (1, 1)
    )
    logger.info(f"Downloading votings from {sitting} sitting")
    while True:
        resp = requests.get(f"{settings.VOTINGS_URL}/{sitting}/{number}")
        logger.debug(
            f"Downloaded voting {sitting}/{number}, {resp.url}, {resp.status_code}"
        )
        if resp.status_code == 404 and number > 1:
            sitting += 1
            number = 1
            continue
        if resp.status_code == 404 or resp.json() == []:
            logger.info(f"Finished downloading votings from {sitting} sitting")
            break
        resp.raise_for_status()
        json_data = resp.json()
        voting = Voting.from_api_response(json_data)
        number += 1
