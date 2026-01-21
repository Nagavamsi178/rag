from typing import List
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever

class ThresholdRetriever(BaseRetriever):
    def __init__(self, db, threshold: float = 0.35, k: int = 6):
        self.db = db
        self.threshold = threshold
        self.k = k

    def _get_relevant_documents(self, query: str) -> List[Document]:
        docs_and_scores = self.db.similarity_search_with_score(
            query,
            k=self.k
        )

        return [
            doc for doc, score in docs_and_scores
            if score >= self.threshold
        ]

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self._get_relevant_documents(query)
