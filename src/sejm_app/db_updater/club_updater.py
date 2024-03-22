from django.conf import settings
from loguru import logger
import requests
from sejm_app import models
from django.db.models import Model
from .db_updater_task import DbUpdaterTask
from django.core.files.base import ContentFile


class ClubUpdaterTask(DbUpdaterTask):
    MODEL: Model = models.Club
    SKIP_BY_DEFAULT = True

    def run(self, *args, **kwargs):
        logger.info("Updating clubs")
        self._download_clubs()

    def _download_photo(self, club: models.Club):
        if club.photo:
            return
        photo_url = f"{settings.CLUBS_URL}/{club.id}/logo"
        photo = requests.get(photo_url)
        logger.info(f"Downloading photo for {club.id}")
        if photo.status_code == 200:
            photo_file = ContentFile(photo.content)
            club.photo.save(f"{club.id}.jpg", photo_file)
            club.save()
        else:
            logger.warning(f"Photo for {club.id} not found")

    def _download_clubs(self):
        logger.info(f"Calling {settings.CLUBS_URL}")
        clubs = requests.get(settings.CLUBS_URL).json()
        for club in clubs:
            if club_model := self.MODEL.objects.filter(id=club["id"]).first():
                for key, value in club.items():
                    setattr(club_model, key, value)
                club_model.save()

            else:
                club_model, _ = self.MODEL.objects.update_or_create(**club)
            self._download_photo(club_model)
