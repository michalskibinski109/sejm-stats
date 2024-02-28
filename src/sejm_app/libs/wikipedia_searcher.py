import wikipedia
from loguru import logger
from sejm_app.models import Envoy


def get_wikipedia_biography(envoy: str) -> str:
    wikipedia.set_lang("pl")
    logger.debug(f"Searching for: {envoy}")
    page_name = wikipedia.search(envoy)[0]
    logger.debug(f"Found page: {page_name}")
    res = wikipedia.page(page_name)
    biography = res.section("Życiorys")
    logger.debug(f"biography: {biography[:10]}")
    if not biography:
        biography = res.summary if res.summary else "-"
    return biography
