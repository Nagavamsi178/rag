def extract_page_citations(context_docs):
    return sorted({
        doc.metadata.get("page")
        for doc in context_docs
        if doc.metadata.get("page") is not None
    })
