from __future__ import annotations
from django.db import models
from .print_model import PrintModel
from sejm_app.utils import camel_to_snake, parse_all_dates
from django.utils.functional import cached_property
from loguru import logger
from .stage import Stage


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

    # web_generated_date = models.DateTimeField()
    def __str__(self):
        return f"{self.id} {self.title}"

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
        process.id = str(response["term"]) + str(response["number"])
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
