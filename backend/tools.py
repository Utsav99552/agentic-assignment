import fitz
import easyocr

reader = easyocr.Reader(['en'])

def extract_pdf_text(pdf_path):
    text = ""

    pdf = fitz.open(pdf_path)

    for page in pdf:
        text += page.get_text()

    return text


def extract_image_text(image_path):

    result = reader.readtext(image_path)

    text = " ".join(
        [item[1] for item in result]
    )

    return text