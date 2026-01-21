# 📄 DocuMind

**Secure, Multi‑User RAG (Retrieval‑Augmented Generation) PDF Chat Application**

DocuMind is an end‑to‑end **document intelligence system** that allows users to upload PDFs and chat with them using **RAG architecture**. It supports **user authentication**, **secure file storage**, **FAISS vector search**, **streaming responses**, and **citation‑aware answers** — all built with **Streamlit + LangChain**.

This project is designed to be **production‑ready**, modular, and extensible for enterprise document QA systems.

---

## 🚀 Key Features

- 🔐 User authentication & role handling
- 📄 Upload and manage multiple PDFs per user
- 🧠 RAG‑based question answering
- 🔍 FAISS vector search (per‑document isolation)
- 📚 Page‑level citations in answers
- ⚡ Streaming AI responses (token‑by‑token)
- 🗂️ Persistent vector stores
- 🧾 Prompt history storage
- 🐳 Docker‑ready deployment

---

## 🧱 Tech Stack

### Core
- **Python 3.10**
- **Streamlit** (UI)
- **LangChain 0.2.x** (RAG orchestration)
- **OpenAI / LLMs** (via LangChain)

### NLP & Vector Search
- Sentence‑Transformers
- HuggingFace Transformers
- FAISS (CPU)

### Security & Auth
- Passlib (bcrypt hashing)
- Custom permission checks

### Storage
- SQLite (users & history)
- File‑system based document storage
- FAISS local vectorstores

---

## 📁 Project Structure

```
documind/
│── main.py                  # Streamlit entry point
│── Dockerfile               # Container setup
│── requirements.txt
│── .env                     # Environment variables (NOT committed)
│── users.db                 # Auth & user metadata
│
├── auth/                     # Authentication & user services
│   ├── db.py
│   └── service.py
│
├── config/                   # App & RAG configuration
│   ├── settings.py
│   └── constants.py
│
├── rag/                      # RAG pipeline
│   ├── loader.py             # PDF loading
│   ├── splitter.py           # Text chunking
│   ├── embeddings.py         # Embedding model
│   ├── vectorstore.py        # FAISS store logic
│   ├── retriever.py          # Similarity search
│   └── chain.py              # RAG chain assembly
│
├── security/                 # Security utilities
│   ├── hashing.py
│   └── permissions.py
│
├── storage/                  # Persistent storage
│   ├── user_files.py         # User‑specific PDF storage
│   └── history.py            # Prompt / chat history
│
├── utils/                    # Supporting utilities
│   ├── cache.py
│   ├── streaming.py
│   ├── citations.py
│   ├── definition_fallback.py
│   ├── logging.py
│   └── exceptions.py
│
└── vectorstores/              # FAISS indexes (per document)
    └── <hash>/{index.faiss,index.pkl}
```

---

## 🧠 How DocuMind Works (RAG Flow)

```
User Query
   ↓
Document Retriever (FAISS)
   ↓
Relevant Chunks
   ↓
Prompt Assembly
   ↓
LLM Generation (Streaming)
   ↓
Answer + Citations
```

Each document is:
- Chunked
- Embedded
- Stored in its own FAISS index

This ensures **isolation, accuracy, and scalability**.

---

## ⚙️ Installation & Local Setup

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd documind
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv documind
documind\Scripts\activate   # Windows
# source documind/bin/activate  # macOS/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=sk-xxxxxx
```

⚠️ **Never commit `.env`**

---

### 5️⃣ Run the Application

```bash
streamlit run main.py
```

App will be available at:
```
http://localhost:8501
```

---



## 🔐 Security Notes

Do **NOT** commit:

- `.env`
- `users.db`
- `vectorstores/`
- Uploaded PDFs
- `__pycache__/`

All sensitive data is user‑isolated.

---

## 🧪 Key Capabilities Explained

### 🔍 Citations
Answers include page‑level citations extracted from source documents.

### ⚡ Streaming
Responses stream token‑by‑token for better UX.

### 🧾 Definition Fallback
If retrieval fails, a fallback definition‑based response is provided.

---

## 🚀 Production Recommendations

- Use PostgreSQL instead of SQLite
- Move vectorstores to object storage
- Add JWT / OAuth auth layer
- Use OpenAI embeddings for higher accuracy
- Add rate‑limiting

---

## 📜 License

This project is proprietary and intended for internal, demo, or client use.

---

## 🤝 Maintained By

**ForgeByte AI**

