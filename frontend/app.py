import streamlit as st
import requests
import time

st.set_page_config(page_title="Agentic AI Assistant")

BACKEND_URL = "https://agentic-assignment.onrender.com"

st.title("Agentic AI Assistant")

@st.cache_data(ttl=60)
def wake_backend():
    try:
        requests.get(f"{BACKEND_URL}/", timeout=30)
    except Exception:
        pass

wake_backend()

query = st.text_input("Enter Query")

document_files = st.file_uploader(
    "Upload PDF / Images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

audio_files = st.file_uploader(
    "Upload Audio Files",
    type=["mp3", "wav", "m4a"],
    accept_multiple_files=True
)

if st.button("Run"):
    files = []
    if document_files:
        for file in document_files:
            files.append(("files", (file.name, file.getvalue(), file.type)))
    if audio_files:
        for file in audio_files:
            files.append(("files", (file.name, file.getvalue(), file.type)))

    with st.spinner("Processing... (may take 20-30s on first request)"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                data={"query": query},
                files=files if files else None,
                timeout=120
            )
            if response.status_code != 200:
                st.error(f"Server error {response.status_code}: {response.text}")
            else:
                result = response.json()
                st.subheader("Plan")
                plan = result.get("plan", [])
                st.write(", ".join(plan) if plan else "No files processed")
                st.subheader("Extracted Text")
                extracted = result.get("extracted_text", "").strip()
                if extracted:
                    with st.expander("Show extracted text"):
                        st.write(extracted)
                else:
                    st.write("No text extracted")
                st.subheader("Answer")
                st.markdown(result.get("answer", "No answer returned"))
        except requests.exceptions.Timeout:
            st.error("Request timed out. Wait 30 seconds and try again.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Try again in a moment.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
