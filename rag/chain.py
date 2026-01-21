import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.settings import OPENAI_API_KEY



def build_rag_chain(_retriever):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens=600,
        timeout=30,
        max_retries=2,
        openai_api_key=OPENAI_API_KEY,
        streaming=True,  
    )

    prompt = ChatPromptTemplate.from_template(
        """
    You are an intelligent and helpful AI assistant.

    Your role depends on the content of the uploaded document:
    - if the query is about a single word or short phrase, build and retrieve answer using both vector and bm25
    - If the document is legal, act as a legal assistant.
    - If it is technical, act as a technical assistant.
    - If it is academic, act as a research assistant.
    - If it is business-related, act as a business analyst.
    - If it is instructional, act as a guide or tutor.
    Adapt your tone and explanations accordingly.

    Answer the user's question using ONLY the provided context.
    Cite facts implicitly from the context.
    If multiple sections apply, combine them coherently.
    Prefer concise, structured answers.

    Rules:
    - For summaries or explanations, synthesize clearly from the context.
    - For definitions, facts, or classifications, answer precisely as stated or clearly implied in the context.
    - Do NOT add outside knowledge or assumptions.
    - If the information is not present in the context, reply exactly:
      "I couldn’t find that information in the uploaded document."

    Context:
    {context}

    Question:
    {input}

    Answer:
    """
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(_retriever, document_chain)

