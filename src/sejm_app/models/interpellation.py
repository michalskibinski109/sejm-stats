from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger
from django.utils.functional import cached_property
from sejm_app.utils import parse_all_dates, camel_to_snake
from sejm_app.models.envoy import Envoy


class Reply(models.Model):
    interpolation = models.ForeignKey(
        "Interpellation", on_delete=models.CASCADE, related_name="replies"
    )
    key = models.CharField(max_length=255)
    receipt_date = models.DateTimeField()
    last_modified = models.DateTimeField()
    from_member = models.ForeignKey(
        Envoy, on_delete=models.CASCADE, related_name="replies", null=True
    )
    body_link = models.URLField(null=True)
    only_attachment = models.BooleanField(default=False)
    attachments = models.JSONField(default=list)

    def __str__(self):
        return self.key

    @classmethod
    def from_api_response(cls, response: dict, interpolation):
        response = parse_all_dates(response)
        response["interpolation"] = interpolation
        response = {camel_to_snake(key): value for key, value in response.items()}
        if "from" in response:
            value = response["from"]
            del response["from"]
            if value.isdigit():
                response["from_member"] = Envoy.objects.get(id=value)
            else:
                try:
                    first_name, last_name = value.split(" ")[-2:]
                    logger.debug(f"first_name: {first_name}, last_name: {last_name}")
                    response["from_member"] = Envoy.objects.get(
                        first_name=first_name, last_name=last_name
                    )
                except Envoy.DoesNotExist:
                    logger.error(
                        f"Envoy with first_name={first_name} and last_name={last_name} does not exist."
                    )
        if "links" in response:
            for link in response["links"]:
                if link["rel"] == "body":
                    response["body_link"] = link["href"]
            del response["links"]
        reply = cls.objects.create(**response)
        return reply


class Interpellation(models.Model):
    term = models.IntegerField(help_text=_("Parliamentary term"), null=True)
    num = models.IntegerField(help_text=_("Interpellation number"), null=True)
    title = models.CharField(
        max_length=255, help_text=_("Title of the interpellation"), null=True
    )
    receipt_date = models.DateTimeField(help_text=_("Date of receipt"), null=True)
    last_modified = models.DateTimeField(help_text=_("Last modified date"), null=True)
    body_link = models.URLField(
        help_text=_("Link to the interpellation body"), null=True
    )
    from_member = models.ForeignKey(
        Envoy, on_delete=models.CASCADE, related_name="interpellations", null=True
    )
    to = models.JSONField(
        default=list, help_text=_("Recipients of the interpellation"), null=True
    )
    sent_date = models.DateTimeField(help_text=_("Date sent"), null=True)
    repeated_interpellation = models.JSONField(
        default=list, help_text=_("Repeated interpellation references"), null=True
    )
    id = models.CharField(max_length=255, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        self.id = f"{self.term}{self.num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.receipt_date})"

    # Rest of your code...
    @classmethod
    def from_api_response(cls, response: dict):
        interpellation = cls()
        response = parse_all_dates(response)
        response = {camel_to_snake(key): value for key, value in response.items()}

        for key, value in response.items():
            if key == "from":
                key = "from_member"
                value = value[0]
                if value.isdigit():
                    value = Envoy.objects.get(id=value)
                elif isinstance(value, str):
                    first_name, last_name = value.split(" ")[-2:]
                    value = Envoy.objects.get(
                        first_name=first_name, last_name=last_name
                    )
                else:
                    logger.debug(f"Could not parse envoy from {value}")
                    continue
            elif key == "replies":
                continue

            elif key == "links":
                for link in value:
                    if link["rel"] == "body":
                        interpellation.body_link = link["href"]
            elif not hasattr(interpellation, key):
                logger.debug(f"Interpellation has no attribute {key}")
                continue

            setattr(interpellation, key, value)

        interpellation.save()

        if "replies" in response:
            for reply_data in response["replies"]:
                reply = Reply.from_api_response(reply_data, interpellation)

        return interpellation
