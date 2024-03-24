from django.utils.dateparse import parse_datetime, parse_date
from django.utils import timezone
from datetime import datetime


def camel_to_snake(name: str) -> str:
    if len(name) < 4 and all([i.isupper() for i in name]):
        return name
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def parse_all_dates(response: dict, only_date=False) -> dict:
    for key, value in response.items():
        if (
            isinstance(value, str)
            and (("date" in key.lower()) or ("last_modified" in key.lower()))
            or ("lastmodified" in key.lower())
        ):
            value = parse_datetime(value) if "T" in value else parse_date(value)
            if isinstance(value, datetime):
                value = timezone.make_aware(value)
            if only_date:
                try:
                    value = value.date()
                except AttributeError:
                    pass
        response[key] = value

    return response
