from django.utils.dateparse import parse_datetime, parse_date


def camel_to_snake(name: str) -> str:
    if len(name) < 4 and all([i.isupper() for i in name]):
        return name
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def parse_all_dates(response: dict) -> dict:
    for key, value in response.items():
        if isinstance(value, str) and ("date" in key):
            value = parse_datetime(value) if "T" in value else parse_date(value)
        response[key] = value
    return response