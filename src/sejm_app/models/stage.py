from __future__ import annotations
from django.db import models
from django.db.models import Max
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
    def from_api_response(cls, response: dict, process):
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

    @property
    def result(self):
        pass_phrases = ("uchwalon", "przyjęto", "przyjeto")
        fail_phrases = ("nie przyjęto", "nie przyjeto", "odrzucon")
        if self.decision:
            if any(phrase in self.decision.lower() for phrase in pass_phrases):
                return "PASS"
            if any(phrase in self.decision.lower() for phrase in fail_phrases):
                return "FAIL"
        return ""

    def __str__(self) -> str:
        return f"{self.process.id} stage {self.stage_number}: {self.stage_name}"
