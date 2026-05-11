# RAG Pipeline: Hybrid Search (Semantic + Lexical)
#
# Preprocessing:
#   1. Load document
#   2. Chunk by section
#   3. Generate embeddings for each chunk
#   4. Store embeddings + text in VectorIndex and BM25Index via Retriever
#
# Query-time:
#   1. Embed user query
#   2. Search both indexes in parallel
#   3. Merge results using Reciprocal Rank Fusion (RRF)
#   4. Inject top chunks into prompt
#
# Cosine similarity: 1.0 = identical direction, -1.0 = opposite, 0.0 = perpendicular
# Cosine distance = 1 - cosine similarity  (closer to 0 = more similar)

import math
import re
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

import voyageai
from dotenv import load_dotenv

load_dotenv()
client = voyageai.Client()


# --- Chunking ---

def chunk_by_section(document_text: str) -> List[str]:
    return re.split(r"\n## ", document_text)


# --- Embedding ---

def generate_embedding(chunks, model="voyage-3-large", input_type="query"):
    is_list = isinstance(chunks, list)
    input_ = chunks if is_list else [chunks]
    result = client.embed(input_, model=model, input_type=input_type)
    return result.embeddings if is_list else result.embeddings[0]


# --- VectorIndex (semantic search) ---

class VectorIndex:
    def __init__(self, distance_metric: str = "cosine", embedding_fn=None):
        self.vectors: List[List[float]] = []
        self.documents: List[Dict[str, Any]] = []
        self._vector_dim: Optional[int] = None
        if distance_metric not in ["cosine", "euclidean"]:
            raise ValueError("distance_metric must be 'cosine' or 'euclidean'")
        self._distance_metric = distance_metric
        self._embedding_fn = embedding_fn

    def add_document(self, document: Dict[str, Any]):
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided during initialization.")
        if not isinstance(document, dict) or "content" not in document:
            raise ValueError("Document must be a dict with a 'content' key.")
        if not isinstance(document["content"], str):
            raise TypeError("Document 'content' must be a string.")
        vector = self._embedding_fn(document["content"])
        self.add_vector(vector=vector, document=document)

    def add_documents(self, documents: List[Dict[str, Any]]):
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided during initialization.")
        if not documents:
            return
        for i, doc in enumerate(documents):
            if not isinstance(doc, dict) or "content" not in doc:
                raise ValueError(f"Document at index {i} must be a dict with a 'content' key.")
            if not isinstance(doc["content"], str):
                raise TypeError(f"Document 'content' at index {i} must be a string.")
        vectors = self._embedding_fn([doc["content"] for doc in documents])
        for vector, document in zip(vectors, documents):
            self.add_vector(vector=vector, document=document)

    def add_vector(self, vector, document: Dict[str, Any]):
        if not isinstance(vector, list) or not all(isinstance(x, (int, float)) for x in vector):
            raise TypeError("Vector must be a list of numbers.")
        if not isinstance(document, dict) or "content" not in document:
            raise ValueError("Document must be a dict with a 'content' key.")
        if not self.vectors:
            self._vector_dim = len(vector)
        elif len(vector) != self._vector_dim:
            raise ValueError(f"Dimension mismatch: expected {self._vector_dim}, got {len(vector)}")
        self.vectors.append(list(vector))
        self.documents.append(document)

    def search(self, query: Any, k: int = 1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []
        if isinstance(query, str):
            if not self._embedding_fn:
                raise ValueError("Embedding function not provided for string query.")
            query_vector = self._embedding_fn(query)
        elif isinstance(query, list) and all(isinstance(x, (int, float)) for x in query):
            query_vector = query
        else:
            raise TypeError("Query must be a string or list of numbers.")
        if self._vector_dim is None or len(query_vector) != self._vector_dim:
            raise ValueError("Query vector dimension mismatch.")
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        dist_func = self._cosine_distance if self._distance_metric == "cosine" else self._euclidean_distance
        distances = [(dist_func(query_vector, v), self.documents[i]) for i, v in enumerate(self.vectors)]
        distances.sort(key=lambda x: x[0])
        return [(doc, dist) for dist, doc in distances[:k]]

    def _euclidean_distance(self, vec1, vec2):
        return math.sqrt(sum((p - q) ** 2 for p, q in zip(vec1, vec2)))

    def _dot_product(self, vec1, vec2):
        return sum(p * q for p, q in zip(vec1, vec2))

    def _magnitude(self, vec):
        return math.sqrt(sum(x * x for x in vec))

    def _cosine_distance(self, vec1, vec2):
        mag1, mag2 = self._magnitude(vec1), self._magnitude(vec2)
        if mag1 == 0 and mag2 == 0:
            return 0.0
        if mag1 == 0 or mag2 == 0:
            return 1.0
        similarity = self._dot_product(vec1, vec2) / (mag1 * mag2)
        return 1.0 - max(-1.0, min(1.0, similarity))

    def __len__(self):
        return len(self.vectors)

    def __repr__(self):
        return f"VectorIndex(count={len(self)}, dim={self._vector_dim}, metric='{self._distance_metric}')"


# --- BM25Index (lexical search) ---

class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75, tokenizer: Optional[Callable] = None):
        self.documents: List[Dict[str, Any]] = []
        self._corpus_tokens: List[List[str]] = []
        self._doc_len: List[int] = []
        self._doc_freqs: Dict[str, int] = {}
        self._avg_doc_len: float = 0.0
        self._idf: Dict[str, float] = {}
        self._index_built: bool = False
        self.k1 = k1
        self.b = b
        self._tokenizer = tokenizer or self._default_tokenizer

    def _default_tokenizer(self, text: str) -> List[str]:
        tokens = re.split(r"\W+", text.lower())
        return [t for t in tokens if t]

    def _update_stats_add(self, doc_tokens: List[str]):
        self._doc_len.append(len(doc_tokens))
        seen = set()
        for token in doc_tokens:
            if token not in seen:
                self._doc_freqs[token] = self._doc_freqs.get(token, 0) + 1
                seen.add(token)
        self._index_built = False

    def _build_index(self):
        if not self.documents:
            self._avg_doc_len = 0.0
            self._idf = {}
            self._index_built = True
            return
        self._avg_doc_len = sum(self._doc_len) / len(self.documents)
        N = len(self.documents)
        self._idf = {
            term: math.log(((N - freq + 0.5) / (freq + 0.5)) + 1)
            for term, freq in self._doc_freqs.items()
        }
        self._index_built = True

    def add_document(self, document: Dict[str, Any]):
        if not isinstance(document, dict) or "content" not in document:
            raise ValueError("Document must be a dict with a 'content' key.")
        if not isinstance(document["content"], str):
            raise TypeError("Document 'content' must be a string.")
        doc_tokens = self._tokenizer(document["content"])
        self.documents.append(document)
        self._corpus_tokens.append(doc_tokens)
        self._update_stats_add(doc_tokens)

    def add_documents(self, documents: List[Dict[str, Any]]):
        if not documents:
            return
        for i, doc in enumerate(documents):
            if not isinstance(doc, dict) or "content" not in doc:
                raise ValueError(f"Document at index {i} must be a dict with a 'content' key.")
            if not isinstance(doc["content"], str):
                raise TypeError(f"Document 'content' at index {i} must be a string.")
            doc_tokens = self._tokenizer(doc["content"])
            self.documents.append(doc)
            self._corpus_tokens.append(doc_tokens)
            self._update_stats_add(doc_tokens)
        self._index_built = False

    def _compute_bm25_score(self, query_tokens: List[str], doc_index: int) -> float:
        score = 0.0
        doc_term_counts = Counter(self._corpus_tokens[doc_index])
        doc_length = self._doc_len[doc_index]
        for token in query_tokens:
            if token not in self._idf:
                continue
            tf = doc_term_counts.get(token, 0)
            score += (self._idf[token] * tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * (doc_length / self._avg_doc_len)) + 1e-9
            )
        return score

    def search(self, query: Any, k: int = 1, score_normalization_factor: float = 0.1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents:
            return []
        if not isinstance(query, str):
            raise TypeError("Query must be a string for BM25Index.")
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        if not self._index_built:
            self._build_index()
        if self._avg_doc_len == 0:
            return []
        query_tokens = self._tokenizer(query)
        if not query_tokens:
            return []
        raw_scores = [
            (self._compute_bm25_score(query_tokens, i), self.documents[i])
            for i in range(len(self.documents))
        ]
        raw_scores = [(s, d) for s, d in raw_scores if s > 1e-9]
        raw_scores.sort(key=lambda x: x[0], reverse=True)
        results = [(doc, math.exp(-score_normalization_factor * score)) for score, doc in raw_scores[:k]]
        results.sort(key=lambda x: x[1])
        return results

    def __len__(self):
        return len(self.documents)

    def __repr__(self):
        return f"BM25Index(count={len(self)}, k1={self.k1}, b={self.b})"


# --- Retriever (hybrid: RRF merge) ---

class SearchIndex(Protocol):
    def add_document(self, document: Dict[str, Any]) -> None: ...
    def add_documents(self, documents: List[Dict[str, Any]]) -> None: ...
    def search(self, query: Any, k: int = 1) -> List[Tuple[Dict[str, Any], float]]: ...


class Retriever:
    def __init__(self, *indexes: SearchIndex):
        if not indexes:
            raise ValueError("At least one index must be provided.")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        for index in self._indexes:
            index.add_document(document)

    def add_documents(self, documents: List[Dict[str, Any]]):
        for index in self._indexes:
            index.add_documents(documents)

    def search(self, query_text: str, k: int = 1, k_rrf: int = 60) -> List[Tuple[Dict[str, Any], float]]:
        if not isinstance(query_text, str):
            raise TypeError("Query text must be a string.")
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        all_results = [index.search(query_text, k=k * 5) for index in self._indexes]

        doc_ranks: Dict[int, Dict] = {}
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                doc_id = id(doc)
                if doc_id not in doc_ranks:
                    doc_ranks[doc_id] = {"doc_obj": doc, "ranks": [float("inf")] * len(self._indexes)}
                doc_ranks[doc_id]["ranks"][idx] = rank + 1

        scored = [
            (entry["doc_obj"], sum(1.0 / (k_rrf + r) for r in entry["ranks"] if r != float("inf")))
            for entry in doc_ranks.values()
        ]
        scored = [(doc, score) for doc, score in scored if score > 0]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


# --- Main ---

with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)

vector_index = VectorIndex(embedding_fn=generate_embedding)
bm25_index = BM25Index()

retriever = Retriever(bm25_index, vector_index)
retriever.add_documents([{"content": chunk} for chunk in chunks])

results = retriever.search("What did the software engineering dept do last year?", k=2)

for doc, score in results:
    print(score, "\n", doc["content"][:200], "\n----\n")
# To improve the quality of search we are going to implement the lexical search as well with semantic search
# semantic search = embeddings + vector db
# lexical search = classic text search
# and in the end merge both results

# Lexical search - In rag pipelines most commonly used method is bm25(best match 25) method.
# User query -> tokenize( break into different word) -> check the frequency -> mark weightage as high and low