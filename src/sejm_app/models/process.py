from __future__ import annotations
from django.db import models
from django.db.models import Max
from .print_model import PrintModel
from .voting import Voting
from django.utils.dateparse import parse_date, parse_datetime
from sejm_app.utils import camel_to_snake, parse_all_dates
from loguru import logger


class Stage(models.Model):
    process = models.ForeignKey(
        "Process", on_delete=models.CASCADE, null=True, related_name="stages"
    )
    stage_number = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    stage_name = models.CharField(max_length=255)
    sitting_num = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    decision = models.CharField(max_length=255, null=True, blank=True)
    text_after_3 = models.URLField(null=True, blank=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # only for new objects
            max_stage_number = (
                self.process.stages.aggregate(Max("stage_number"))["stage_number__max"]
                or 0
            )
            self.stage_number = max_stage_number + 1
        super().save(*args, **kwargs)

    @classmethod
    def from_api_response(cls, response: dict, process: Process):
        stage = cls()
        if len(response.get("children", ())) > 1:
            logger.error(f"More than one child in stage for {process.id}")
            return
        if len(response.get("children", ())) > 0:
            child = response["children"][0]
            response.pop("children")
            for key in response.keys():
                if key in child:
                    del child[key]
            response.update(child)
        response = parse_all_dates(response)
        response = {camel_to_snake(key): value for key, value in response.items()}
        for key, value in response.items():
            if key == "voting" and value:
                if Voting.objects.filter(title=value["title"]).exists():
                    value = Voting.objects.filter(title=value["title"]).first()
                else:
                    value = Voting.from_api_response(value)
            if not hasattr(stage, key):
                logger.debug(f"Stage has no attribute {key}")
                continue

            setattr(stage, key, value)
        process.save()
        stage.process = process
        stage.save()
        return stage


class Process(models.Model):
    """
    api https://api.sejm.gov.pl/sejm/openapi/ui/#/default/get_sejm_term_term__processes__num_
    """

    id = models.CharField(max_length=10, primary_key=True, unique=True)
    UE = models.BooleanField(
        choices=((True, "YES"), (False, "NO")), null=True, blank=True
    )
    change_date = models.DateTimeField()
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

    @classmethod
    def from_api_response(cls, response: dict):
        process = cls()
        response = parse_all_dates(response)
        response["UE"] = response["UE"] == "YES"
        response = {camel_to_snake(key): value for key, value in response.items()}
        process.id = str(response["term"]) + str(response["number"])
        for key, value in response.items():
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
