from langchain_community.embeddings import SentenceTransformerEmbeddings
from utils.cache import get_embeddings

def load_embeddings():
    return get_embeddings()
