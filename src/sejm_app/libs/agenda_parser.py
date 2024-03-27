import re
from bs4 import BeautifulSoup


def parse_agenda(agenda):
    soup = BeautifulSoup(agenda, "html.parser")
    divs = soup.find_all("div")
    text_lines = [div.get_text() for div in divs]
    readable_agenda = "\n".join(text_lines)

    return readable_agenda


def get_print_ids_from_agenda(agenda) -> list[int]:
    titles = re.findall(r"\(druki? nr [\d, i]+\)", agenda)
    print_ids = []
    for title in titles:
        ids = re.findall(r"\d+", title)
        print_ids.extend(ids)
    return print_ids
