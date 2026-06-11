# 🤖 Agentic AI Assistant

A full-stack AI-powered document and media analysis tool. Upload PDFs, images, or audio files and ask anything — the assistant extracts content and gives structured, intelligent answers powered by the Cerebras inference API.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Docker Setup](#docker-setup)
- [API Reference](#api-reference)
- [Supported Query Types](#supported-query-types)
- [Supported File Types](#supported-file-types)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)

---

## Overview

Agentic AI Assistant is a multimodal AI pipeline that accepts documents, images, and audio as input, extracts their content automatically, and then uses a large language model to answer user queries about that content in a structured, professional format.

The backend is a FastAPI REST API that handles file ingestion and orchestrates the AI pipeline. The frontend is a Streamlit web app that provides a clean, simple interface for users to upload files and ask questions.

---

## Features

- **PDF Text Extraction** — extracts full text from uploaded PDF files using PyMuPDF
- **Image OCR** — reads text from images (PNG, JPG, JPEG) using EasyOCR
- **Audio Transcription** — converts MP3, WAV, and M4A audio to text using Faster Whisper
- **Multi-file support** — upload multiple files at once; all content is combined before querying
- **Structured AI Responses** — the agent follows strict output rules based on query intent (summaries, sentiment, code analysis, resume parsing, comparisons, and more)
- **Query-aware formatting** — answers are always returned in clean markdown, never raw HTML
- **Fast inference** — powered by Cerebras `gpt-oss-120b` running at ~3000 tokens/second

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM Inference | Cerebras API (`gpt-oss-120b`) |
| PDF Extraction | PyMuPDF (`fitz`) |
| Image OCR | EasyOCR |
| Speech-to-Text | Faster Whisper |
| HTTP Client | Requests |
| Server | Uvicorn |

---

## Project Structure

```
agentic-assignment/
│
├── backend/
│   ├── __init__.py       # Makes backend a Python package
│   ├── agent.py          # LLM client + prompt logic (Cerebras API)
│   ├── main.py           # FastAPI app, routes, file handling
│   └── tools.py          # PDF extraction, OCR, speech-to-text
│
├── frontend/
│   └── app.py            # Streamlit UI
│
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container setup (runs both services)
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- A **Cerebras API key** — get one free at [cloud.cerebras.ai](https://cloud.cerebras.ai)
- `ffmpeg` installed on your system (required by Faster Whisper for audio processing)

**Install ffmpeg:**

```bash
# Ubuntu / Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html and add to PATH
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/agentic-assignment.git
cd agentic-assignment
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

> **Note:** EasyOCR and Faster Whisper will download their model weights on first use. EasyOCR downloads ~100MB and Whisper base model downloads ~150MB. This only happens once and is cached locally.

---

## Configuration

Set your Cerebras API key as an environment variable before starting the server.

**Linux / macOS:**

```bash
export CEREBRAS_API_KEY=your_api_key_here
```

**Windows (Command Prompt):**

```cmd
set CEREBRAS_API_KEY=your_api_key_here
```

**Windows (PowerShell):**

```powershell
$env:CEREBRAS_API_KEY="your_api_key_here"
```

**To make it permanent**, add the export line to your `~/.bashrc`, `~/.zshrc`, or system environment variables.

You can verify the key is correctly set by running:

```bash
curl https://api.cerebras.ai/v1/models \
  -H "Authorization: Bearer $CEREBRAS_API_KEY"
```

You should see a list of available models including `gpt-oss-120b`.

---

## Running the App

You need two terminals — one for the backend and one for the frontend.

**Terminal 1 — Start the FastAPI backend:**

```bash
uvicorn backend.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Terminal 2 — Start the Streamlit frontend:**

```bash
streamlit run frontend/app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Docker Setup

To run everything in a single container:

**1. Build the image:**

```bash
docker build -t agentic-ai .
```

**2. Run the container:**

```bash
docker run -p 8000:8000 -p 8501:8501 \
  -e CEREBRAS_API_KEY=your_api_key_here \
  agentic-ai
```

Then open [http://localhost:8501](http://localhost:8501).

---

## API Reference

The FastAPI backend exposes the following endpoints:

### `GET /`
Health check — confirms the server is running.

**Response:**
```json
{ "message": "Agent Running" }
```

---

### `POST /chat`
Main endpoint. Accepts a query and optional files, extracts content, and returns an AI-generated answer.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | Yes | The question or instruction for the AI |
| `files` | `file[]` | No | One or more PDF, image, or audio files |

**Response:**
```json
{
  "plan": ["PDF Extraction", "OCR"],
  "extracted_text": "Full extracted text from all uploaded files...",
  "answer": "AI-generated structured response in markdown..."
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/chat \
  -F "query=Summarize this document" \
  -F "files=@report.pdf"
```

---

## Supported Query Types

The agent automatically detects the intent of your query and formats the response accordingly:

| Query Type | What to Ask | Response Format |
|---|---|---|
| **Summary** | "Summarize this", "Give me a summary" | One-line summary, 3 bullet points, 5-sentence summary |
| **Sentiment** | "What is the sentiment?", "Analyze the tone" | Sentiment label, confidence score, justification |
| **Code Analysis** | "Analyze this code", "Find bugs" | Explanation, bugs found, time complexity |
| **Technical Skills** | "Extract skills from this resume" | Bullet list of all technical skills |
| **Resume Breakdown** | "Explain this resume" | Education, Skills, Projects, Experience, Achievements |
| **Strengths** | "What are the strengths?" | Key strengths identified |
| **Weaknesses** | "What are the weaknesses?" | Areas of improvement |
| **Comparison** | "Compare these two documents" | Side-by-side table, strengths, weaknesses, recommendation |
| **General Q&A** | Any custom question | Structured, professional answer |

---

## Supported File Types

| Category | Extensions |
|---|---|
| Documents | `.pdf` |
| Images | `.png`, `.jpg`, `.jpeg` |
| Audio | `.mp3`, `.wav`, `.m4a` |

Multiple files can be uploaded at once. Their extracted content is combined and sent to the LLM as a single context window.

---

## How It Works

```
User uploads file(s) + types a query
          │
          ▼
   FastAPI /chat endpoint
          │
          ▼
  For each file, detect type:
  ┌───────────────────────────────┐
  │ .pdf   → PyMuPDF extraction   │
  │ image  → EasyOCR              │
  │ audio  → Faster Whisper STT   │
  └───────────────────────────────┘
          │
          ▼
  All extracted text combined
          │
          ▼
  Prompt built with content + query
          │
          ▼
  Cerebras API (gpt-oss-120b)
  ~3000 tokens/second inference
          │
          ▼
  Structured markdown answer
  returned to Streamlit UI
```

---

## Troubleshooting

**`CEREBRAS_API_KEY` not found / Missing credentials error**

The API key environment variable is not set in the current shell session. Run:
```bash
export CEREBRAS_API_KEY=your_key_here
```
Then restart uvicorn in the same terminal.

---

**`Model gpt-oss-120b does not exist` error**

Your API key may not have access to this model, or the model ID has changed. Check the current list of available models:
```bash
curl https://api.cerebras.ai/v1/models \
  -H "Authorization: Bearer $CEREBRAS_API_KEY"
```
Update the `model=` value in `backend/agent.py` to match a model from the response.

---

**`ModuleNotFoundError: No module named 'backend'`**

You must run uvicorn from the **project root directory** (the folder that contains the `backend/` folder), not from inside `backend/` itself:
```bash
# Correct — run from project root
cd agentic-assignment
uvicorn backend.main:app --reload --port 8000
```

---

**`Could not connect to the backend` in Streamlit**

The FastAPI server is not running or is on a different port. Make sure Terminal 1 shows uvicorn running on port 8000 before using the Streamlit UI.

---

**EasyOCR or Whisper slow on first run**

Both models download weights on first use (~100–150MB each). Subsequent runs will be fast as the models are cached locally. If you're on a CPU-only machine, OCR and transcription will be slower than on a GPU.

---

**`ffmpeg not found` error during audio transcription**

Install ffmpeg and ensure it's on your system PATH. See the [Prerequisites](#prerequisites) section.
