import re
import unicodedata

def normalize_text(text: str):
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)  # remove HTML
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)  # zero width chars
    text = re.sub(r"[<>;]", "", text)
    return text.strip()

