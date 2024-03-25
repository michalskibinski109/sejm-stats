from django.conf import settings
from loguru import logger
import requests
from sejm_app import models
from django.db.models import Model

from sejm_app.libs.wikipedia_searcher import get_wikipedia_biography
from sejm_app.models.club import Club
from .db_updater_task import DbUpdaterTask
from django.core.files.base import ContentFile
from django.db import transaction


class EnvoyUpdaterTask(DbUpdaterTask):
    # DEPENDS ON ClubUpdaterTask
    MODEL: Model = models.Envoy
    SKIP_BY_DEFAULT = True

    def run(self, *args, **kwargs):
        logger.info("Updating envoys")
        with transaction.atomic():
            self._download_envoys()

    def _download_photo(self, envoy: models.Envoy):
        if envoy.photo:
            return
        photo_url = f"{settings.ENVOYS_URL}/{envoy.id}/photo"
        photo = requests.get(photo_url)
        logger.info(f"Downloading photo for {envoy.id}")
        if photo.status_code == 200:
            photo_file = ContentFile(photo.content)
            envoy.photo.save(f"{envoy.id}.jpg", photo_file)
            envoy.save()
        else:
            logger.warning(f"Photo for {envoy.id} not found")

    def _download_biography(self, envoy: models.Envoy):
        if envoy.biography:
            return
        biography, source = get_wikipedia_biography(envoy.title, with_source=True)
        envoy.biography = biography
        envoy.biography_source = source
        envoy.save()

    def _download_envoys(self):
        logger.info(f"Calling {settings.ENVOYS_URL}")
        envoys = requests.get(settings.ENVOYS_URL).json()
        for envoy in envoys:
            envoy.pop("firstLastName", None)
            envoy.pop("lastFirstName", None)
            envoy["club"] = Club.objects.get(id=envoy["club"])
            if not self.MODEL.objects.filter(id=envoy["id"]).exists():
                envoy_model = self.MODEL.objects.create(**envoy)
                self._download_biography(envoy_model)
                self._download_photo(envoy_model)
                envoy_model.save()
            else:
                envoy_model = self.MODEL.objects.get(id=envoy["id"])
                for key, value in envoy.items():
                    setattr(envoy_model, key, value)
                envoy_model.save()
