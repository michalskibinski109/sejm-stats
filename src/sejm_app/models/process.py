from __future__ import annotations
from django.db import models
from .print_model import PrintModel
from sejm_app.utils import camel_to_snake, parse_all_dates
from django.utils.functional import cached_property
from loguru import logger
from .stage import Stage
from .envoy import Envoy
from .club import Club
from eli_app.libs.pdf_parser import get_pdf_authors


class CreatedByEnum(models.TextChoices):
    ENVOYS = "posłowie"
    CLUB = "klub"
    PRESIDIUM = "prezydium"
    CITIZENS = "obywatele"
    GOVERNMENT = "rząd"


class Process(models.Model):
    """
    api https://api.sejm.gov.pl/sejm/openapi/ui/#/default/get_sejm_term_term__processes__num_
    """

    id = models.CharField(max_length=10, primary_key=True, unique=True)
    UE = models.BooleanField(
        choices=((True, "YES"), (False, "NO")), null=True, blank=True
    )
    comments = models.TextField()
    number = models.IntegerField()
    term = models.IntegerField()
    webGeneratedDate = models.DateTimeField(null=True, blank=True)
    changeDate = models.DateField(null=True)
    description = models.TextField()
    documentDate = models.DateField()
    documentType = models.CharField(max_length=255)
    legislativeCommittee = models.BooleanField()
    printModel = models.ForeignKey(
        PrintModel, on_delete=models.CASCADE, blank=True, null=True
    )
    principleOfSubsidiarity = models.BooleanField()
    processStartDate = models.DateField()
    urgencyWithdrawDate = models.DateField(null=True, blank=True)
    rclNum = models.CharField(max_length=20)
    title = models.TextField()
    urgencyStatus = models.CharField(max_length=20)
    MPs = models.ManyToManyField(Envoy, related_name="processes", blank=True)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="processes", null=True, blank=True
    )
    createdBy = models.CharField(
        max_length=20,
        choices=CreatedByEnum.choices,
        null=True,
        blank=True,
        default=None,
    )

    # web_generated_date = models.DateTimeField()
    def __str__(self):
        return f"{self.id} {self.title}"

    def save(self, *args, **kwargs):
        # self.createdBy = self._get_type_of_process()
        # logger.debug(f"Created by: {self.createdBy}")
        # self._assign_authors()
        return super().save(*args, **kwargs)

    # def _assign_authors(self) -> None:
    #     if self.createdBy == CreatedByEnum.CLUB:
    #         for club in Club.objects.all():
    #             if club.name.lower() in self.title.lower():
    #                 self.club = club
    #                 return
    #     if self.createdBy == CreatedByEnum.ENVOYS:
    #         envoys = Envoy.objects.all()
    #         possible_authors = get_pdf_authors(self.print.pdf_url)
    #         for author in possible_authors:
    #             first_name, last_name = author.split(" ")[0], author.split(" ")[-1]
    #             if envoy := envoys.filter(
    #                 firstName__iexact=first_name, lastName__iexact=last_name
    #             ).first():
    #                 try:

    #                     self.MPs.add(envoy)
    #                 except ValueError as e:
    #                     logger.error(f"Error while adding {envoy} to process: {e}")

    # def _get_type_of_process(self) -> str:
    #     if self.documentType.lower() not in [
    #         "projekt ustawy",
    #         "wniosek",
    #         "projekt uchwały",
    #     ]:
    #         return
    #     if self.title.lower().startswith("poselski"):
    #         return CreatedByEnum.ENVOYS
    #     if "prezydium sejmu" in self.title.lower():
    #         return CreatedByEnum.PRESIDIUM
    #     if "obywatelski" in self.title.lower():
    #         return CreatedByEnum.CITIZENS
    #     if "rządowy" in self.title.lower():
    #         return CreatedByEnum.GOVERNMENT
    #     if "przez klub parlamentarny" in self.title.lower():
    #         return CreatedByEnum.CLUB

    @property
    def print(self):
        return PrintModel.objects.get(id=self.id)

    @cached_property
    def is_finished(self) -> bool:
        if not self.stages.exists():
            return False
        return self.stages.last().stageName.lower() == "zamknięcie sprawy"
