import PyPDF2
from transformers import pipeline, SummarizationPipeline
import requests
from loguru import logger
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_name = "allenai/led-large-16384-arxiv"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)


def extract_text_from_pdf(pdf_path):
    pdf_file_obj = open(pdf_path, "rb")
    # ...
    logger.info(f"Extracting text from pdf")
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    # remove headers and footers
    for page in pdf_reader.pages:
        page.mediabox.lower_left = (
            page.mediabox.left,
            page.mediabox.bottom + 50,
        )
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file_obj.close()
    logger.debug(f"Pdf text: {text}")
    return text


# ...


def summarize_text(text):
    text = text.replace("\xa0", " ")
    model = "sshleifer/distilbart-cnn-12-6"
    summarizer: SummarizationPipeline = pipeline("summarization", model=model)

    summary = summarizer(text, max_length=480, min_length=30, do_sample=False)
    return summary[0]["summary_text"]


def summarize_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    return summary


# resp = requests.get("https://api.sejm.gov.pl/eli/acts/DU/2023/3/text.pdf", stream=True)
# with open("myfile.pdf", "wb") as f:
#     f.write(resp.content)
# pdf = resp.content
# logger.info("Downloaded pdf")


# # Write the bytes to a file
# with open("temp.pdf", "wb") as f:
#     f.write(pdf)
# print(summarize_pdf("temp.pdf"))
text = """
. 1. W przypadku egzaminu zawodowego przeprowadzanego w okresie od dnia 9 stycznia 2023 r. do
dnia 31 stycznia 2023 r. asystentowi technicznemu biorącemu udział w przeprowadzaniu części praktycznej tego
egzaminu, której rezultatem końcowym wykonania zadania lub zadań egzaminacyjnych jest wyrób lub usługa, w tym
dla osób, które zdają ten egzamin jako eksternistyczny, przysługuje wynagrodzenie w wysokości określonej jako
iloczyn 0,54% stawki za każdą godzinę udziału w jednej zmianie egzaminu, zgodnie z czasem trwania części praktycznej egzaminu zawodowego, określonym w informatorze, o którym mowa w art. 9a ust. 2 pkt 3 ustawy z dnia
7 września 1991 r. o systemie oświaty, na podstawie art. 44zzzm ust. 3 tej ustawy, oraz liczby zmian egzaminu,
w których bierze udział.
2. Asystentowi technicznemu, o którym mowa w ust. 1, przysługuje także wynagrodzenie w wysokości określonej jako iloczyn 0,54% stawki za każdą godzinę przygotowywania stanowisk egzaminacyjnych dla jednej zmiany
egzaminu oraz liczby zmian egzaminu, w których bierze udział. Czas przygotowywania stanowisk egzaminacyjnych
dla jednej zmiany egzaminu nie może być dłuższy niż trzy godziny.
3. W przypadku egzaminu potwierdzającego kwalifikacje w zawodzie przeprowadzanego w okresie od dnia
9 stycznia 2023 r. do dnia 31 stycznia 2023 r. przepisy ust. 1 i 2 stosuje się również do asystentów technicznych,
o których w § 1 ust. 2 pkt 2.”."""
print(summarize_text(text))
