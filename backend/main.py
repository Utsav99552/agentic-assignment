from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.tools import (
    extract_pdf_text,
    extract_image_text,
    extract_audio_text
)
from backend.agent import ask_agent   # FIX: was ask_gemini — function was renamed

import tempfile
import os
import shutil

app = FastAPI()

# FIX: Add CORS middleware so Streamlit (port 8501) can call FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Agent Running"}


@app.post("/chat")
async def chat(
    query: str = Form(...),
    files: list[UploadFile] = File([])
):
    extracted_text = ""
    plan = []

    # FIX: Use a temp directory so files are always saved to a writable,
    # predictable location regardless of where FastAPI is launched from.
    temp_dir = tempfile.mkdtemp()

    try:
        for file in files:
            filename = file.filename
            temp_path = os.path.join(temp_dir, filename)

            with open(temp_path, "wb") as f:
                f.write(await file.read())

            # PDF
            if filename.lower().endswith(".pdf"):
                plan.append("PDF Extraction")
                extracted_text += "\n\n" + extract_pdf_text(temp_path)

            # Image OCR
            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                plan.append("OCR")
                extracted_text += "\n\n" + extract_image_text(temp_path)

            # Audio Speech-to-Text
            elif filename.lower().endswith((".mp3", ".wav", ".m4a")):
                plan.append("Speech To Text")
                extracted_text += "\n\n" + extract_audio_text(temp_path)

    finally:
        # Clean up temp files after processing
        shutil.rmtree(temp_dir, ignore_errors=True)

    if not query:
        return {
            "follow_up": "What would you like me to do with the uploaded content?"
        }

    answer = ask_agent(extracted_text, query)   # FIX: was ask_gemini

    return {
        "plan": plan,
        "extracted_text": extracted_text,
        "answer": answer
    }