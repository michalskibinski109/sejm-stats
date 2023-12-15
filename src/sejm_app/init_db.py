# import django settings
from django.conf import settings
import requests
from sejm_app.models import Club, Envoy, Vote, Voting, VotingOption
from loguru import logger
from django.db.utils import OperationalError
import io
from django.core.files.base import ContentFile
import urllib.parse as urlparse
from django.utils import timezone
from datetime import datetime


def camel_to_snake(name):
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def run():
    try:
        Club.objects.first()
        Voting.objects.first()
    except OperationalError:
        logger.info("Database not initialized yet")
        return
    download_clubs()
    download_envoys()
    download_photos()
    download_clubs_photos()
    # download_votings()


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
            Envoy.objects.create(**envoy)
    else:
        logger.info("Envoys already exists in database")


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


# def create_voting_option(option, voting_obj):
#     option["voting"] = voting_obj
#     VotingOption.objects.create(**option)


def create_vote(vote, voting_obj):
    vote["voting"] = voting_obj
    Vote.objects.create(**vote).save()


def process_votes(votes):
    for vote in votes:
        vote["MP"] = Envoy.objects.get(id=vote["MP"])
        if vote["vote"] == "VOTE_VALID":
            vote["vote"] = list(vote["listVotes"].values())[-1]  # get only last value
        for field in ["club", "firstName", "lastName", "mP", "listVotes", "secondName"]:
            if field in vote:
                vote.pop(field)

        vote["vote"] = VotingOption[vote["vote"].upper()].value
    return votes


def process_voting_json_data(json_data):
    date_str = json_data["date"]
    date_format = "%Y-%m-%dT%H:%M:%S"
    naive_date = datetime.strptime(date_str, date_format)
    json_data["date"] = timezone.make_aware(naive_date)
    for field in [
        "notParticipating",
        "totalVoted",
        "term",
        "votingOptions",
    ]:
        if field in json_data:
            json_data.pop(field)

    return json_data


def download_votings():
    last_voting = (
        Voting.objects.order_by("-date").first() if Voting.objects.exists() else None
    )
    # check if last voting is from today
    if last_voting and last_voting.date.date() == timezone.now().date():
        logger.info("Votings are up to date")
        return
    sitting, number = (
        (last_voting.sitting, last_voting.votingNumber + 1) if last_voting else (1, 1)
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
        votes = process_votes(json_data.pop("votes"))
        logger.debug(f"Votes for {sitting}/{number}: {len(votes)}")
        json_data = process_voting_json_data(json_data)

        voting_obj = Voting.objects.create(**json_data)
        # for option in options:
        #     create_voting_option(option, voting_obj)
        for vote in votes:
            create_vote(vote, voting_obj)
        voting_obj.save()
        number += 1
