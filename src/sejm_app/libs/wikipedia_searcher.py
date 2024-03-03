import wikipedia
from loguru import logger
from sejm_app.models import Envoy


def get_wikipedia_biography(envoy: str, with_source: bool = False) -> str:
    wikipedia.set_lang("pl")
    logger.debug(f"Searching for: {envoy}")
    page_name = wikipedia.search(envoy)[0]
    logger.debug(f"Found page: {page_name}")
    res = wikipedia.page(page_name)
    biography = res.section("Życiorys")

    if not biography:
        biography = res.summary if res.summary else "-"
    if with_source:
        return biography, res.url
    logger.debug(f"biography: {biography[:10]}")
    return biography
