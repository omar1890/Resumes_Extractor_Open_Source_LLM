from PyPDF2 import PdfReader
from PIL import Image
import pytesseract


def extract_text(path, ext):
    text = ""
    if ext == ".pdf":
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
    return text.strip()
