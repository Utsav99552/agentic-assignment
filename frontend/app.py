import streamlit as st
import requests

st.title("Agentic AI Assistant")

query = st.text_input("Enter Query")

uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True
)

if st.button("Run"):

    files = []

    if uploaded_files:
        for file in uploaded_files:
            files.append(
                (
                    "files",
                    (
                        file.name,
                        file,
                        file.type
                    )
                )
            )

    response = requests.post(
        "http://localhost:8000/chat",
        data={"query": query},
        files=files
    )

    result = response.json()

    st.subheader("Plan")
    st.write(result.get("plan"))

    st.subheader("Extracted Text")
    st.write(result.get("extracted_text"))

    st.subheader("Answer")
    st.write(result.get("answer"))