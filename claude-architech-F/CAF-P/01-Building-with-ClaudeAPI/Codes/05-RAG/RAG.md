# Retrieval Augmented Generation (RAG)

RAG lets you work with documents too large to fit in a single prompt by breaking them into chunks and retrieving only the most relevant pieces at query time.

## The Problem

Large documents (e.g. an 800-page financial report) can't be stuffed into a prompt wholesale. Simply including everything hits hard context limits, degrades response quality, and increases cost and latency.

## Two Approaches

| Approach | How it works | Drawback |
|---|---|---|
| **Prompt stuffing** | Dump the full document into every prompt | Hits context limits; slow and expensive |
| **RAG** | Preprocess → chunk → retrieve relevant pieces → include only those | Requires upfront engineering |

With RAG, a question like *"What risks does this company face?"* fetches only the Risk Factors chunk — not all 800 pages.

## How RAG Works

1. **Preprocess** — split the document into chunks (by size, by section headers, etc.)
2. **Search** — find chunks most relevant to the user's question
3. **Prompt** — inject only those chunks alongside the question

## Trade-offs

**Benefits**
- Scales to very large or multiple documents
- Claude focuses on relevant content only
- Smaller prompts = lower cost + faster responses

**Challenges**
- Preprocessing and a search mechanism are required
- Chunking strategy matters — wrong chunks = missing context
- More implementation complexity than prompt stuffing

## When to Use RAG

Use RAG when documents are too large for the context window, when you're querying across multiple documents, or when cost/latency is a concern. For small documents that fit comfortably in a prompt, simple stuffing is often fine.

> **Key insight:** RAG trades simplicity for scalability. More upfront work, but it enables document collections that prompt stuffing can't handle.

---

## Text Chunking Strategies

Chunking is the most critical step in a RAG pipeline — bad chunks mean irrelevant context, which means wrong answers. For example, a query about software bugs could return medical research content if a medical section also uses the word "bug."

### Strategy Comparison

| Strategy | How it works | Best for | Downside |
|---|---|---|---|
| **Size-based** | Split into equal-length strings | Any document type; reliable fallback | Cuts mid-sentence; loses context |
| **Structure-based** | Split on headers/sections (e.g. `## `) | Well-formatted docs (Markdown, reports) | Breaks on unstructured text/PDFs |
| **Sentence-based** | Split on sentence boundaries, group N sentences | General text; good middle ground | Sentences can vary wildly in length |
| **Semantic-based** | NLP to group related sentences | Highest quality chunks | Expensive and complex to implement |

### Size-Based (with overlap)

Overlap carries context across chunk boundaries — prevents words and sentences from being cut off cold.

```python
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks, start_idx = [], 0
    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunks.append(text[start_idx:end_idx])
        start_idx = end_idx - chunk_overlap if end_idx < len(text) else len(text)
    return chunks
```

### Structure-Based

```python
def chunk_by_section(document_text):
    return re.split(r"\n## ", document_text)
```

### Sentence-Based (with overlap)

```python
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, start_idx = [], 0
    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        chunks.append(" ".join(sentences[start_idx:end_idx]))
        start_idx = max(0, start_idx + max_sentences_per_chunk - overlap_sentences)
    return chunks
```

### Semantic-Based

Split text into sentences, then use NLP to measure similarity between consecutive sentences, grouping related ones into chunks. Produces the most contextually coherent chunks but is computationally expensive and complex to implement — not a common first choice for production.

### Choosing a Strategy

- **Control document format?** → Structure-based gives cleanest results
- **General text?** → Sentence-based is a solid middle ground
- **Unknown/mixed content or code?** → Size-based with overlap is the safest default

> There's no universal best strategy. Size-based with overlap is the common production default — simple, reliable, and works with anything.

---

## Retrieval: Finding Relevant Chunks

After chunking, you need to find which chunks best answer a user's question. This is a search problem.

### Semantic Search vs Keyword Search

Keyword search matches exact words — fragile and context-blind. **Semantic search** uses embeddings to match *meaning*, so a question about "financial risk" can match a chunk that never uses those exact words.

### Text Embeddings

An embedding converts text into a list of numbers (floats between -1 and +1) that encodes its meaning. Similar texts produce numerically similar embeddings, enabling mathematical comparison.

- Feed text into an embedding model → get back a vector of numbers
- Each dimension captures some learned feature of the text (not human-interpretable)
- Compare embeddings with cosine similarity to rank chunk relevance

### Generating Embeddings with VoyageAI

Anthropic doesn't provide embeddings — the recommended provider is **VoyageAI**.

**Setup:**
```bash
pip install voyageai
```

Add to `.env`:
```
VOYAGE_API_KEY="your_key_here"
```

**Usage:**
```python
from dotenv import load_dotenv
import voyageai

load_dotenv()
client = voyageai.Client()

def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]
```

Use `input_type="query"` for user questions and `input_type="document"` for chunks — VoyageAI optimizes embeddings differently for each.

> Next step: compare the query embedding against all chunk embeddings (cosine similarity) to rank and retrieve the most relevant chunks.

---

## Complete RAG Pipeline: End-to-End Walkthrough

A full RAG pipeline has two phases — **preprocessing** (done once, ahead of time) and **query-time** (done per request).

### Phase 1: Preprocessing (Offline)

| Step | What happens |
|---|---|
| **1. Chunk** | Split source documents into sections (e.g., by size or header) |
| **2. Embed** | Run each chunk through an embedding model → get a vector per chunk |
| **3. Store** | Save vectors + source text in a vector database |

### Phase 2: Query-Time (Per Request)

| Step | What happens |
|---|---|
| **4. Embed query** | Run user's question through the same embedding model |
| **5. Search** | Vector DB finds chunks with highest cosine similarity to the query vector |
| **6. Prompt** | Inject retrieved chunk(s) + question into the final prompt → send to Claude |

### How Similarity Works: Cosine Similarity

Vectors are **normalized** (scaled to magnitude 1.0) before comparison. Similarity is then measured by the cosine of the angle between two vectors.

| Value | Meaning |
|---|---|
| Close to **1** | High similarity |
| Close to **0** | No relationship |
| Close to **-1** | Opposite meaning |

**Cosine distance** = `1 - cosine similarity` — used in vector DB docs where smaller = more similar.

**Example:**
- Medical chunk → `[0.944, 0.331]`
- Software chunk → `[0.295, 0.955]`
- User query "what did the software dept do?" → `[0.112, 0.993]`
- Similarity to software chunk: **0.983** ✅ — Similarity to medical chunk: **0.398** ❌

The software chunk is returned and injected into the prompt.

### Final Prompt Structure

```
Answer the user's question using only the context below.

<question>{user_question}</question>

<context>{retrieved_chunk}</context>
```

> **Key insight:** Semantic similarity — not keyword matching — drives retrieval. Chunks that share *meaning* with the query score high even if they share no exact words.

---

## RAG Implementation: Code Walkthrough

Five steps to go from raw document to working retrieval.

### Step 1: Chunk the Document

```python
with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)
```

Uses `chunk_by_section` from earlier — splits on section headers.

### Step 2: Generate Embeddings (Batch)

```python
embeddings = generate_embedding(chunks)  # accepts list or single string
```

### Step 3: Build the Vector Store

```python
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
```

> Always store the **original text** alongside the embedding — search returns the text, not the numbers.

### Step 4: Embed the User Query

```python
user_embedding = generate_embedding("What did the software engineering dept do last year?")
```

Must use the **same embedding model** as Step 2.

### Step 5: Search and Retrieve

```python
results = store.search(user_embedding, 2)  # top-2 results

for doc, distance in results:
    print(distance, doc["content"][:200])
```

**Sample output:**
```
0.71  ## Section 2: Software Engineering ...
0.72  ## Methodology ...
```

Lower cosine distance = higher similarity. Section 2 wins at 0.71.

### Summary

| Step | Action | Key point |
|---|---|---|
| 1 | Chunk | Split doc into sections |
| 2 | Embed chunks | Batch process all chunks |
| 3 | Store | Save embedding + source text together |
| 4 | Embed query | Same model as Step 2 |
| 5 | Search | Returns top-N chunks by cosine distance |

> RAG is fundamentally: text → numbers → store → search → retrieve → prompt.

---

## Hybrid Search: Semantic + BM25 Lexical

Semantic search alone fails on exact term lookups. Searching for `INC-2023-Q4-011` might return a semantically related financial section that never mentions the ID. The fix: run both semantic and lexical search in parallel and merge results.

| Method | Strength | Weakness |
|---|---|---|
| **Semantic** | Finds conceptually related content | May miss exact/rare terms |
| **Lexical (BM25)** | Finds exact term matches | Ignores meaning and context |
| **Hybrid** | Best of both | More implementation complexity |

### How BM25 Works

BM25 (Best Match 25) ranks documents by term frequency, weighted by rarity:

1. **Tokenize** query → `["a", "INC-2023-Q4-011"]`
2. **Count** how often each term appears across all chunks
3. **Weight** — rare terms score higher, common words ("a", "the") score low
4. **Rank** chunks by weighted term frequency

Result: `INC-2023-Q4-011` gets high weight (rare) → chunks containing it rank first.

### BM25 Implementation

```python
# 1. Chunk text
chunks = chunk_by_section(text)

# 2. Build BM25 index
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})

# 3. Search
results = store.search("What happened with INC-2023-Q4-011?", 3)

for doc, distance in results:
    print(distance, doc["content"][:200])
```

BM25 correctly surfaces the cybersecurity and software engineering sections that actually contain the incident ID — sections semantic search would have ranked lower.

> **Rule of thumb:** Use semantic search for conceptual queries; add BM25 when users may look up IDs, codes, names, or exact phrases. Hybrid covers both.

### The Retriever: Unified Hybrid Interface

`VectorIndex` and `BM25Index` share the same API (`add_document`, `add_documents`, `search`). The `Retriever` class exploits this to coordinate both indexes behind a single interface — any index implementing the `SearchIndex` protocol can be plugged in.

```python
retriever = Retriever(bm25_index, vector_index)
retriever.add_documents([{"content": chunk} for chunk in chunks])
results = retriever.search("What happened with INC-2023-Q4-011?", k=2)
```

Internally, `search` fans out to all indexes, collects ranked lists, and merges them with RRF.

### Merging Results: Reciprocal Rank Fusion (RRF)

RRF combines ranked lists from multiple indexes without needing comparable scores — cosine distance and BM25 scores live on different scales, so raw score averaging is meaningless. RRF uses only rank positions.

**Formula:**
```
RRF_score(d) = Σ  1 / (k + rank_i(d))
```
`k` is a smoothing constant (default 60); higher = less weight on top ranks.

**Worked example** — query: `"INC-2023-Q4-011"`

| Chunk | VectorIndex rank | BM25 rank | RRF score (k=1) |
|---|---|---|---|
| Section 2 | 1 | 2 | 1/(1+1) + 1/(1+2) = **0.833** |
| Section 6 | 3 | 1 | 1/(1+3) + 1/(1+1) = **0.750** |
| Section 7 | 2 | 3 | 1/(1+2) + 1/(1+3) = **0.583** |

Final order: Section 2 → Section 6 → Section 7. Section 2 ranks well in both, so it wins.

**Result vs semantic-only:** hybrid correctly surfaces the software engineering section as #2; vector-only returned an unrelated financial section there instead.

### Extensibility

Any class implementing `add_document` + `search` can be added to `Retriever` — keyword index, graph-based search, domain-specific index. The RRF merge handles the rest automatically.
