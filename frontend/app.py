import streamlit as st
import requests

st.set_page_config(page_title="Agentic AI Assistant")

st.title("Agentic AI Assistant")

query = st.text_input("Enter Query")

# PDF / Image Upload
document_files = st.file_uploader(
    "Upload PDF / Images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Audio Upload
audio_files = st.file_uploader(
    "Upload Audio Files",
    type=["mp3", "wav", "m4a"],
    accept_multiple_files=True
)

if st.button("Run"):

    files = []

    # PDF / Images
    if document_files:
        for file in document_files:
            files.append(
                ("files", (file.name, file.getvalue(), file.type))
            )

    # Audio
    if audio_files:
        for file in audio_files:
            files.append(
                ("files", (file.name, file.getvalue(), file.type))
            )

    try:
        response = requests.post(
            "https://agentic-assignment-production.up.railway.app/chat",  # ← your Railway URL
            data={"query": query},
            files=files if files else None
        )

        # FIX: Check HTTP status before attempting to parse JSON.
        # Previously, a 422 or 500 from FastAPI would cause an unhandled
        # crash inside response.json() with a confusing error message.
        if response.status_code != 200:
            st.error(
                f"Server error {response.status_code}: {response.text}"
            )
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

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the backend. "
            "Make sure FastAPI is running on http://localhost:8000"
        )
    except Exception as e:
        st.error(f"Unexpected error: {e}")