import os
import hashlib
import streamlit as st

from auth.db import init_db
from auth.service import verify_user, register_user, get_user_role

from storage.user_files import (
    get_user_dir,
    save_uploaded_file,
    list_accessible_pdfs,
    resolve_pdf_path,
)

from storage.history import save_prompt_history, get_prompt_history
from utils.citations import extract_page_citations
from utils.definition_fallback import find_definition
from utils.streaming import StreamlitCallbackHandler

from rag.loader import load_pdf_documents
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vectorstore import load_or_create_vectorstore
from rag.chain import build_rag_chain


# ---------------- INIT ----------------
init_db()
st.set_page_config(page_title="DocuMind", page_icon="🔐")

# ---------------- SESSION ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("role", "user")


# ---------------- QUERY INTENT ----------------
def detect_query_intent(query: str) -> str:
    q = query.lower()

    if any(p in q for p in ["who is defined", "what is defined", "definition of"]):
        return "definition"

    if any(p in q for p in ["what type of", "classified as"]):
        return "classification"

    if any(p in q for p in [
        "what is this document about",
        "summary",
        "summarize",
        "overview",
        "purpose of this document",
        "what does this document describe",
    ]):
        return "summary"

    return "factual"


# ---------------- PDF HASH (CRITICAL FIX) ----------------
def get_pdf_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ---------------- AUTH ----------------
if not st.session_state.logged_in:
    st.title("🔐 Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = get_user_role(u)
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(u, p):
                st.success("Registered successfully")
            else:
                st.error("Username already exists")

    st.stop()


# ---------------- SIDEBAR ----------------
st.sidebar.write(
    f"👤 **{st.session_state.username}** ({st.session_state.role})"
)

if st.session_state.role == "admin":
    st.sidebar.success("🛡 Admin Access Enabled")


# ---------------- FILE UPLOAD ----------------
user_dir = get_user_dir(st.session_state.username)

uploaded = st.sidebar.file_uploader("📤 Upload PDF", type="pdf")
if uploaded:
    save_uploaded_file(uploaded, user_dir)
    st.sidebar.success("PDF uploaded successfully!")


# ---------------- PDF LIST ----------------
pdf_refs = list_accessible_pdfs(
    role=st.session_state.role,
    current_user=st.session_state.username,
)

selected_pdf = st.sidebar.selectbox("📄 Select a PDF", options=pdf_refs)


# ---------------- RAG WORKFLOW ----------------
if selected_pdf:
    try:
        pdf_path = resolve_pdf_path(
            pdf_ref=selected_pdf,
            role=st.session_state.role,
            current_user=st.session_state.username,
        )
    except PermissionError:
        st.error("🚫 Unauthorized access to document")
        st.stop()
    except FileNotFoundError:
        st.error("❌ Document not found")
        st.stop()

    st.info(f"📘 Using document: `{selected_pdf}`")

    documents = load_pdf_documents(
        str(pdf_path),
        os.path.getmtime(pdf_path)
    )
    if not documents:
        st.error("❌ No extractable text found in PDF")
        st.stop()

    chunks = split_documents(documents)
    embeddings = load_embeddings()

    # 🔥 UNIQUE VECTOR STORE PER PDF
    VECTORSTORE_ROOT = "vectorstores"
    os.makedirs(VECTORSTORE_ROOT, exist_ok=True)

    pdf_hash = get_pdf_hash(str(pdf_path))
    store_path = os.path.join(VECTORSTORE_ROOT, pdf_hash)


    db = load_or_create_vectorstore(
        chunks,
        embeddings,
        store_path=store_path,
    )

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 30, "lambda_mult": 0.75,},
    )

    rag_chain = build_rag_chain(retriever)

    with st.form("qa_form"):
        query = st.text_input("Ask a question")
        submitted = st.form_submit_button("Ask")

    if submitted and query:
        intent = detect_query_intent(query)

        with st.spinner("Thinking..."):
            result = rag_chain.invoke({"input": query})
            answer = result["answer"]
            context_docs = result.get("context", [])
            pages = extract_page_citations(context_docs)

            # -------- Classification inference --------
            if intent == "classification" and "couldn’t find" in answer.lower():
                for doc in context_docs:
                    if "open-end mortgage" in doc.page_content.lower():
                        answer = (
                            "This document is classified as an Open-End Mortgage "
                            "under applicable law."
                        )
                        pages = [doc.metadata.get("page")]
                        break

            # -------- Definition fallback --------
            if intent == "definition" and "couldn’t find" in answer.lower():
                term = query.split()[-1].rstrip("?")
                definition = find_definition(documents, term)
                if definition:
                    answer = definition["text"]
                    pages = [definition["page"]]

            # -------- Render --------
            st.markdown("### ✅ Answer")
            st.markdown(answer)

            if pages and "couldn’t find" not in answer.lower():
                st.markdown("#### 📌 Sources")
                st.markdown(", ".join(f"Page {p}" for p in pages))

            save_prompt_history(
                st.session_state.username,
                selected_pdf,
                query,
                answer,
            )


# ---------------- HISTORY ----------------
st.sidebar.subheader("🕘 Prompt History")

history = get_prompt_history(st.session_state.username)

if history:
    for doc, q, a in history:
        with st.sidebar.expander(f"📄 {doc}"):
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
else:
    st.sidebar.info("No history yet.")


