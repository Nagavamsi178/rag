import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

@st.cache_data(show_spinner=False)
def load_pdf_documents(path: str, file_mtime: float):
    loader = PyPDFLoader(path)
    documents = loader.load()

    for doc in documents:
        doc.metadata["page"] = doc.metadata.get("page", 0) + 1

    return documents

