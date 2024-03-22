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
    number = models.IntegerField()
    change_date = models.DateField()
    description = models.TextField()
    # document_date = models.DateField()
    document_type = models.CharField(max_length=255)
    legislative_committee = models.BooleanField()
    print_model = models.ForeignKey(
        PrintModel, on_delete=models.CASCADE, blank=True, null=True
    )
    principle_of_subsidiarity = models.BooleanField()
    process_start_date = models.DateField()
    urgency_withdraw_date = models.DateField(null=True, blank=True)
    rcl_num = models.CharField(max_length=20)
    title = models.TextField()
    urgency_status = models.CharField(max_length=20)
    MPs = models.ManyToManyField(Envoy, related_name="processes", blank=True)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="processes", null=True, blank=True
    )
    created_by = models.CharField(
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
        self.created_by = self._get_type_of_process()
        logger.debug(f"Created by: {self.created_by}")
        self._assign_authors()
        return super().save(*args, **kwargs)

    def _assign_authors(self) -> None:
        if self.created_by == CreatedByEnum.CLUB:
            for club in Club.objects.all():
                if club.name.lower() in self.title.lower():
                    self.club = club
                    return
        if self.created_by == CreatedByEnum.ENVOYS:
            envoys = Envoy.objects.all()
            possible_authors = get_pdf_authors(self.print.pdf_url)
            for author in possible_authors:
                first_name, last_name = author.split(" ")[0], author.split(" ")[-1]
                if envoy := envoys.filter(
                    firstName__iexact=first_name, lastName__iexact=last_name
                ).first():
                    try:

                        self.MPs.add(envoy)
                    except ValueError as e:
                        logger.error(f"Error while adding {envoy} to process: {e}")

    def _get_type_of_process(self) -> str:
        if self.document_type.lower() not in [
            "projekt ustawy",
            "wniosek",
            "projekt uchwały",
        ]:
            return
        if self.title.lower().startswith("poselski"):
            return CreatedByEnum.ENVOYS
        if "prezydium sejmu" in self.title.lower():
            return CreatedByEnum.PRESIDIUM
        if "obywatelski" in self.title.lower():
            return CreatedByEnum.CITIZENS
        if "rządowy" in self.title.lower():
            return CreatedByEnum.GOVERNMENT
        if "przez klub parlamentarny" in self.title.lower():
            return CreatedByEnum.CLUB

    @property
    def print(self):
        return PrintModel.objects.get(id=self.id)

    @cached_property
    def is_finished(self) -> bool:
        if not self.stages.exists():
            return False
        return self.stages.last().stage_name.lower() == "zamknięcie sprawy"

    @classmethod
    def from_api_response(cls, response: dict):
        process = cls()
        response = parse_all_dates(response)
        response["UE"] = response["UE"] == "YES"
        response = {camel_to_snake(key): value for key, value in response.items()}
        process.id = f"{response['term']}{response['number']}"
        for key, value in response.items():
            if key == "change_date":
                value = value.split("T")[0]
            if key == "stages":
                for stage in value:
                    Stage.from_api_response(stage, process)
                continue
            if not hasattr(process, key):
                logger.debug(f"Process has no attribute {key}")
                continue
            # if key == "print_model":
            #     value = PrintModel.objects.get(
            #         term=value["term"], number=value["number"]
            #     )
            if hasattr(process, key):
                setattr(process, key, value)
        process.save()

        return process
