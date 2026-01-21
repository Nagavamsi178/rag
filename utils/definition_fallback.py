import re

def find_definition(documents, term):
    pattern = re.compile(
        rf'\b{re.escape(term)}\b\s+(means|shall mean|is defined as)\s+(.*)',
        re.IGNORECASE
    )

    for doc in documents:
        for line in doc.page_content.splitlines():
            match = pattern.search(line)
            if match:
                return {
                    "text": line.strip(),
                    "page": doc.metadata.get("page"),
                }

    return None
