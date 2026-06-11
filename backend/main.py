from fastapi import FastAPI, UploadFile, File, Form
from backend.tools import *
from backend.agent import ask_gemini

app = FastAPI()


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

    for file in files:

        filename = file.filename

        with open(filename, "wb") as f:
            f.write(await file.read())

        if filename.endswith(".pdf"):
            plan.append("PDF Extraction")
            extracted_text += extract_pdf_text(filename)

        elif filename.endswith(
                (".png", ".jpg", ".jpeg")):
            plan.append("OCR")
            extracted_text += extract_image_text(
                filename
            )

    if not query:
        return {
            "follow_up":
            "What would you like me to do with the uploaded content?"
        }

    answer = ask_gemini(
        extracted_text,
        query
    )

    return {
        "plan": plan,
        "extracted_text": extracted_text,
        "answer": answer
    }