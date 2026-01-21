from pathlib import Path
from langchain_community.vectorstores import FAISS

def load_or_create_vectorstore(documents, embeddings, store_path):
    store_path = Path(store_path)
    store_path.mkdir(parents=True, exist_ok=True)

    index_file = store_path / "index.faiss"
    pkl_file = store_path / "index.pkl"

    if index_file.exists() and pkl_file.exists():
        return FAISS.load_local(
            str(store_path),
            embeddings,
            allow_dangerous_deserialization=True
        )

    db = FAISS.from_documents(documents, embeddings)
    db.save_local(str(store_path))
    return db
