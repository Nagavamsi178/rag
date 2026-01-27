import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter

@st.cache_data(show_spinner=False)
def split_documents(_documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(_documents)
