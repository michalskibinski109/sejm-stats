from django.utils.dateparse import parse_datetime, parse_date
from django.utils import timezone
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils.timezone import localtime
from django.utils.timesince import timesince


def camel_to_snake(name: str) -> str:
    if len(name) < 4 and all([i.isupper() for i in name]):
        return name
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def format_human_friendly_date(date):
    now = localtime()
    date = localtime(date)

    # Using 'naturalday' for 'today', 'yesterday', or 'tomorrow' - or the date
    natural_date = naturalday(date)

    if natural_date == "today":
        natural_date = "dzisiaj"
    elif natural_date == "yesterday":
        natural_date = "wczoraj"
    time_str = date.strftime("%H:%M")
    if natural_date in ["dzisiaj", "wczoraj"]:
        return f"{natural_date} o godz {time_str}"
    else:
        days_ago = timesince(date, now)
        return f"{days_ago} o godz {time_str}"


def parse_all_dates(response: dict, date_only=False) -> dict:
    if not response:
        return response
    for key, value in response.items():
        if (
            (isinstance(value, str) or isinstance(value, datetime))
            and (("date" in key.lower()) or ("modified" in key.lower()))
            or ("modified" in key.lower())
        ):
            value = parse_datetime(value) if "T" in value else parse_date(value)
            if isinstance(value, datetime):
                value = timezone.make_aware(value)
            if date_only:
                try:
                    value = value.date()
                except AttributeError:
                    pass
        response[key] = value

    return response
