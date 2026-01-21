# import streamlit as st
# from langchain_community.embeddings import SentenceTransformerEmbeddings


# def get_embeddings():
#     return SentenceTransformerEmbeddings(
#         model_name="BAAI/bge-large-en-v1.5",
#         encode_kwargs={"normalize_embeddings": True},
#     )


import streamlit as st
from langchain_community.embeddings import SentenceTransformerEmbeddings

@st.cache_resource(show_spinner="Loading embedding model...")
def get_embeddings():
    return SentenceTransformerEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        encode_kwargs={"normalize_embeddings": True},
    )
