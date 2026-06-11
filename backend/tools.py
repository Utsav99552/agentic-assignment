import fitz

# FIX: Lazy-load heavy models — loading at import time causes slow startup
# and crashes if dependencies aren't available yet.
_ocr_reader = None
_whisper_model = None


def _get_ocr_reader():
    global _ocr_reader
    if _ocr_reader is None:
        import easyocr
        _ocr_reader = easyocr.Reader(['en'])
    return _ocr_reader


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        _whisper_model = WhisperModel("base")
    return _whisper_model


# ---------------- PDF ----------------

def extract_pdf_text(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)
    for page in pdf:
        text += page.get_text()
    return text


# ---------------- IMAGE ----------------

def extract_image_text(image_path):
    reader = _get_ocr_reader()
    result = reader.readtext(image_path)
    text = " ".join([item[1] for item in result])
    return text


# ---------------- AUDIO ----------------

def extract_audio_text(audio_path):
    model = _get_whisper_model()
    segments, info = model.transcribe(audio_path)
    text = ""
    for segment in segments:
        text += segment.text + " "
    return text.strip()