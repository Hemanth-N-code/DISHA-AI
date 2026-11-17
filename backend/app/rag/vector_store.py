# backend/app/rag/vector_store.py
import re
import math
from typing import List, Dict, Any, Tuple

class SimpleVectorStore:
    """
    Lightweight, deterministic in-memory vector store with TF-IDF cosine similarity.
    Works offline, has zero external API dependencies, and guarantees instant fast search.
    Can be swapped with pgvector in production deployments.
    """
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.vocabulary: Dict[str, int] = {}
        self.doc_vectors: List[Dict[int, float]] = []
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        return words

    def add_documents(self, docs: List[Dict[str, Any]]):
        """
        docs is a list of dicts: {"id": str, "content": str, "metadata": dict}
        """
        self.documents = docs
        doc_count = len(docs)
        doc_freq: Dict[str, int] = {}

        # 1. Build vocabulary and document frequencies
        tokenized_docs = []
        for d in docs:
            tokens = set(self._tokenize(d["content"]))
            tokenized_docs.append(tokens)
            for t in tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self.vocabulary = {term: idx for idx, term in enumerate(doc_freq.keys())}

        # 2. Compute IDF
        self.idf = {}
        for term, df in doc_freq.items():
            self.idf[term] = math.log((1.0 + doc_count) / (1.0 + df)) + 1.0

        # 3. Compute TF-IDF vectors for documents
        self.doc_vectors = []
        for d in docs:
            tokens = self._tokenize(d["content"])
            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1

            vec: Dict[int, float] = {}
            norm_sq = 0.0
            for term, count in tf.items():
                if term in self.vocabulary:
                    term_idx = self.vocabulary[term]
                    weight = count * self.idf[term]
                    vec[term_idx] = weight
                    norm_sq += weight * weight

            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            for idx in vec:
                vec[idx] /= norm
            self.doc_vectors.append(vec)

    def similarity_search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        if not self.documents or not self.doc_vectors:
            return []

        tokens = self._tokenize(query)
        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1

        query_vec: Dict[int, float] = {}
        norm_sq = 0.0
        for term, count in tf.items():
            if term in self.vocabulary:
                term_idx = self.vocabulary[term]
                weight = count * self.idf[term]
                query_vec[term_idx] = weight
                norm_sq += weight * weight

        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        for idx in query_vec:
            query_vec[idx] /= norm

        scores: List[Tuple[int, float]] = []
        for i, doc_vec in enumerate(self.doc_vectors):
            dot_product = 0.0
            for term_idx, q_val in query_vec.items():
                if term_idx in doc_vec:
                    dot_product += q_val * doc_vec[term_idx]
            scores.append((i, dot_product))

        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_idx, score in scores[:top_k]:
            doc_data = dict(self.documents[doc_idx])
            doc_data["score"] = round(score, 4)
            results.append(doc_data)

        return results

vector_store = SimpleVectorStore()
