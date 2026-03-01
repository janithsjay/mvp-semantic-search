# Technical Selections — MVP Semantic Search

This document outlines the **technical choices** for the MVP semantic search system and the rationale behind each selection. It’s intended to give engineers a clear view of **what is used and why**.

---

## 1. Programming Language

**Choice:** Python  

**Why:**  
- Rich ecosystem for ML and NLP: `sentence-transformers`, `faiss`, `nltk`, `spacy`.  
- Rapid prototyping, easy to iterate on MVP.  
- Easy integration with future APIs, CLI tools, or web interfaces.  

---

## 2. Document Parsing

**Choice:** Python scripts using `markdown` and `BeautifulSoup`  

**Why:**  
- Handles multiple doc formats: Markdown, HTML, or synthetic docs.  
- Lightweight, fast, minimal dependencies.  
- Allows preprocessing: stripping HTML, extracting code blocks, cleaning content.  

---

## 3. Document Chunking

**Choice:** Section + token-based chunking  

- **Chunk size:** 300–400 tokens  
- **Overlap:** 50–100 tokens  

**Why:**  
- Preserves semantic context for each chunk.  
- Prevents information loss at section boundaries.  
- Simple to implement with Python tokenizers (`nltk`, `spacy`, or Hugging Face tokenizers).  

---

## 4. Embedding Model

**Choice:** `all-MiniLM-L6-v2` from Sentence Transformers (Hugging Face)  

**Why:**  
- Bi-encoder transformer → supports fast retrieval.  
- Lightweight and CPU-friendly → suitable for MVP.  
- Pretrained → no fine-tuning required initially.  
- Produces 384-dimensional, L2-normalized vectors suitable for cosine similarity.  

**Future Considerations:**  
- Upgrade to `all-mpnet-base-v2` or `bge-base-en-v1.5` for higher semantic quality.  
- Cross-encoder reranker can improve top-K accuracy but slower and not needed for MVP.  

---

## 5. Vector Index

**Choice:** FAISS (`IndexFlatIP`)  

**Why:**  
- Efficient similarity search for dense embeddings.  
- Simple serialization and deserialization for offline/online pipelines.  
- No need for a full vector database at MVP scale (<50k chunks).  

**Notes:**  
- Metadata stored separately in JSON or SQLite.  
- Can upgrade to IVF/PQ/HNSW FAISS indexes for larger datasets.  

---

## 6. Metadata Storage

**Choice:** JSON files or SQLite DB  

**Why:**  
- Maps vector IDs → original text + metadata (`doc_id`, `section_title`, `position`, `source_url`).  
- Lightweight, portable, and easy to update.  
- Ensures retrieval pipeline can return meaningful info alongside vectors.  

---

## 7. Query Pipeline

**Choice:** Python script  

**Why:**  
- Embeds query with same model + normalization → consistent results.  
- Performs FAISS search → retrieves top-K chunks efficiently.  
- Returns text + metadata in a simple structure.  

**Future Considerations:**  
- Wrap as REST API or FastAPI service for multi-user applications.  
- Add optional cross-encoder reranker for improved accuracy.  

---

## 8. Evaluation / Testing

**Choice:** Small synthetic test set (10–20 queries)  

- **Metrics:** Recall@K, Mean Reciprocal Rank (MRR)  

**Why:**  
- Quick sanity check of retrieval quality.  
- Lightweight, does not require full-scale data or complex setup.  

---

## 9. Folder Structure (Technical Perspective)

```
mvp-semantic-search/
├── data/ # Raw docs (Markdown, HTML, synthetic)
├── chunks/ # Section-level chunks + metadata
├── embeddings/ # Serialized embeddings (.npy, .pt)
├── index/ # FAISS index files (.bin)
├── scripts/ # Pipeline scripts
│ ├── preprocess.py # Load & chunk docs
│ ├── embed.py # Generate embeddings
│ ├── build_index.py # Build FAISS index
│ └── query_index.py # Query + retrieval
├── test_queries/ # Test/evaluation queries
├── TECH_SELECTIONS.md # This technical selection document
├── SI.md # Solution Intent
├── ARCHITECTURE.md # Architecture diagrams
├── README.md # Repo overview & usage
├── requirements.txt # Python dependencies
└── .gitignore
```

**Purpose:**  
- Clear separation of raw data, processed chunks, embeddings, and index.  
- Modular scripts allow easy extension for new documents or alternative embeddings.  

---

### ✅ Summary of Key Technical Selections

| Component           | Choice | Purpose / Why |
|--------------------|--------|----------------|
| Language            | Python | Rich ML ecosystem, fast prototyping |
| Document Parsing    | markdown / BeautifulSoup | Lightweight parsing of multiple doc formats |
| Chunking            | Section + token overlap | Preserves semantic context and prevents info loss |
| Embedding Model     | all-MiniLM-L6-v2 | Lightweight, CPU-friendly, pretrained |
| Vector Index        | FAISS IndexFlatIP | Fast similarity search for MVP-scale embeddings |
| Metadata            | JSON / SQLite | Maps vectors to text + doc info for retrieval |
| Query Pipeline      | Python script | Consistent embedding + search |
| Evaluation          | Recall@K, MRR | Quick sanity check for retrieval quality |

---
