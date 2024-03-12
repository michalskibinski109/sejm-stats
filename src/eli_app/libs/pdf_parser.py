import PyPDF2
from transformers import pipeline, SummarizationPipeline
import requests
from loguru import logger
from pdfminer.high_level import extract_text
import pytesseract
from pdf2image import convert_from_path
import glob
import re


def get_pdf_authors(url: str) -> list:
    file = requests.get(url)
    with open("temp.pdf", "wb") as f:
        f.write(file.content)
    file_path = "temp.pdf"
    text = _extract_text_from_pdf(file_path)
    return _extract_envoys(text)


def _extract_text_from_pdf(file_path: str) -> str:
    try:
        pages = convert_from_path(file_path, 500)
        for page in pages[:3]:
            page.save("out.jpg", "JPEG")
            text = ""
            for pageNum, imgBlob in enumerate(pages[:3]):
                text += pytesseract.image_to_string(imgBlob, lang="pol")

            return text
    except Exception as e:
        logger.error(f"Error while extracting text from pdf: {e}")
        return ""


def _extract_envoys(text: str) -> list:
    # Regular expression pattern to match envoy names
    text = text.replace("\n", " ")
    pattern = r"\(-\)\s([A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ\s]+);"
    matches = re.findall(pattern, text)
    envoys = [match.strip() for match in matches]

    return envoys
