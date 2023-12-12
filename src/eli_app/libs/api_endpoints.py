# {
#     "list_statuses": "https://api.sejm.gov.pl/eli/statuses",
#     "list_reference_types": "https://api.sejm.gov.pl/eli/references",
#     "list_document_types": "https://api.sejm.gov.pl/eli/types",
#     "list_keywords": "https://api.sejm.gov.pl/eli/keywords",
#     "list_institutions": "https://api.sejm.gov.pl/eli/institutions",
#     "list_publishers": "https://api.sejm.gov.pl/eli/acts",
#     "list_years": "https://api.sejm.gov.pl/eli/acts/{publisher}",
#     "list_acts": "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}",
#     "act_details": "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}/{position}",
#     "act_pdf": "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}/{position}/text.pdf",
#     "act_html": "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}/{position}/text.html",
#     "act_references": "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}/{position}/references",
#     "search": "https://api.sejm.gov.pl/eli/acts/search",
#     "list_changed_acts": "https://api.sejm.gov.pl/eli/changes/acts?since={date}&limit={limit}&offset={offset}",
# }
import requests
from urllib.parse import urljoin, urlparse
from datetime import datetime
from pydantic import BaseModel, Field


class EliAPI:
    BASE_URL = "https://api.sejm.gov.pl/eli/"
    DEFAULT_PUBLISHER = "DU"

    def __init__(self):
        self.session = requests.Session()

    def _request(self, endpoint, **kwargs):
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.get(url, params=kwargs)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def list_statuses(self):
        return self._request("statuses")

    def list_reference_types(self):
        return self._request("references")

    def list_document_types(self):
        return self._request("types")

    def list_keywords(self):
        return self._request("keywords")

    def list_institutions(self):
        return self._request("institutions")

    def list_years(self, publisher):
        return self._request(f"acts/{publisher}")

    def list_acts(self, publisher, year):
        return self._request(f"acts/{publisher}/{year}")

    def act_details(self, publisher, year, position):
        return self._request(f"acts/{publisher}/{year}/{position}")

    def act_pdf(self, publisher, year, position):
        return self._request(f"acts/{publisher}/{year}/{position}/text.pdf")

    def act_html(self, publisher, year, position):
        return self._request(f"acts/{publisher}/{year}/{position}/text.html")

    def act_references(self, publisher, year, position):
        return self._request(f"acts/{publisher}/{year}/{position}/references")

    def search(self):
        return self._request("acts/search")

    def list_changed_acts(self, date, limit, offset):
        date_str = date.strftime("%Y-%m-%d")
        return self._request("changes/acts", since=date_str, limit=limit, offset=offset)
