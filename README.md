# Solution Intent — MVP Semantic Search for Technical Documentation

## 1. Problem Statement

Engineers struggle to find relevant information in large technical documentation because:

- Keyword search fails on semantic queries (e.g., “rotate credentials” vs “key renewal process”)  
- Documents are long, hierarchical, and contain code + examples  
- Users want specific, contextually relevant sections  

**Goal:** Build a retrieval-only semantic search system using pretrained embeddings to return the most relevant documentation sections for natural language queries.

---

## 2. Scope

### In-Scope
- Retrieval-only system (no generative or fine-tuned model)  
- Pretrained encoder embeddings (bi-encoder)  
- FAISS vector indexing  
- Section-level chunking with metadata  
- Query → embedding → FAISS search → top-K retrieval  
- MVP evaluation with small synthetic or public docs  

### Out-of-Scope
- Cross-encoder reranking (optional future enhancement)  
- Hybrid search (BM25 + dense)  
- Multi-vector retrieval (ColBERT)  
- Large-scale sharding / cloud deployment  

---

## 3. MVP Goals

- End-to-end retrieval pipeline for technical documentation  
- Low-latency queries (<200ms for small index)  
- Easily swappable dataset (synthetic → real docs)  
- Measurable retrieval quality (Recall@K / MRR)  
- Modular architecture for offline indexing and online querying  

---

## 4. System Architecture

### Offline / Batch Pipeline
1. Document Loader: Load Markdown, HTML, or synthetic docs  
2. Chunking Layer:  
   - Section-level + 300–400 token chunks  
   - 50–100 token overlap  
   - Preserve headings, code blocks, metadata (`doc_id`, `section_title`, `position`)  
3. Embedding Layer:  
   - Bi-encoder model (`all-MiniLM-L6-v2` for MVP)  
   - Tokenization + pooling + L2 normalization  
4. Vector Index (FAISS):  
   - `IndexFlatIP` for MVP  
   - Store chunk vectors + IDs  
5. Persistence: Save FAISS index + metadata for query-time use  

### Online / Query Pipeline
1. Receive user query  
2. Embed query using same model & normalization  
3. FAISS search → top-K chunks (e.g., top 5–10)  
4. Return results with metadata (section title, doc_id, URL)  

### Architecture Diagram
<img width="1349" height="1723" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/46fa18f8-483c-492a-bafa-70e341583f53" />

## 5. Document Chunking Strategy

- Hierarchy-aware: split by headings (H1/H2/H3)  
- Token-based sub-chunks: 300–400 tokens, 50–100 token overlap  
- Preserve code blocks & lists  
- Metadata per chunk: `doc_id`, `section_title`, `position`, `source_url`  
- Rationale: preserves semantic coherence, prevents context loss at boundaries, enables section-level retrieval  

---

## 6. Embedding Model

- Type: Encoder-only transformer, bi-encoder  
- MVP Model: `all-MiniLM-L6-v2`  
- Embedding dim: 384  
- Normalization: L2-normalized for cosine similarity  
- Reason: lightweight, CPU-friendly, fast, works out-of-the-box  
- Future upgrade: `all-mpnet-base-v2` or `bge-base-en-v1.5` for higher quality  

---

## 7. Vector Index (FAISS)

- Index Type: `IndexFlatIP` for MVP  
- Reason: exact similarity search for small dataset  
- Future scaling: IVF / PQ or external vector DB (Milvus, Weaviate)  

---

## 8. Query Processing

1. Query → embed with same model  
2. Search FAISS → top-K candidates  
3. Return chunk text + metadata  

Optional future step: cross-encoder reranker for top-50 candidates  

---

## 9. Evaluation Strategy

- Create small test set: 10–20 synthetic queries → relevant chunks  
- Metrics: Recall@5 / Recall@10, MRR  
- Purpose: validate retrieval quality, sanity check MVP  

---

## 10. Engineering Decisions Summary

| Decision | Choice | Reason |
|----------|--------|--------|
| Retrieval type | Bi-encoder only | Fast, scalable for MVP |
| Chunking | Heading-level + token sub-chunks | Preserve semantics, prevent info loss |
| Chunk size | 300–400 tokens | Balance context and embedding quality |
| Chunk overlap | 50–100 tokens | Prevent boundary context loss |
| Embedding model | all-MiniLM-L6-v2 | Lightweight, CPU-friendly, easy install |
| Embedding normalization | L2-normalized | Enables cosine similarity with inner product |
| Vector index | FAISS IndexFlatIP | Simple, exact search for small MVP |
| Metadata | doc_id, heading, position, URL | Enables UI display, filtering, future reranking |
| Dataset | Synthetic or public docs | No internal data needed for MVP |
| Evaluation | Recall@K, MRR | Quick sanity check of retrieval quality |

---

## 11. Folder Structure

```
mvp-semantic-search/
├── data/                  # Raw input documents (Markdown, HTML, or synthetic docs)
│   ├── example_doc1.md
│   └── example_doc2.md
│
├── chunks/                # Generated document chunks + metadata (JSON/CSV)
│   ├── chunk_0001.json
│   └── chunk_0002.json
│
├── embeddings/            # Serialized embeddings (e.g., .npy, .pt)
│   ├── chunk_embeddings.npy
│   └── embedding_metadata.json
│
├── index/                 # FAISS index files
│   └── faiss_index.bin
│
├── scripts/               # Optional: utility scripts
│   ├── preprocess.py      # Load docs and generate chunks
│   ├── embed.py           # Generate embeddings for chunks
│   ├── build_index.py     # Build FAISS index
│   └── query_index.py     # Query pipeline
│
├── test_queries/          # Test/evaluation queries for MVP
│   └── test_queries.json
│
├── SI.md                  # Solution Intent (this document)
├── ARCHITECTURE.md        # System Architecture diagram and explanation
├── README.md              # Repo overview, installation, usage
├── requirements.txt       # Python dependencies
└── .gitignore

```
---

## ✅ Key Takeaways

- Modular MVP: offline indexing + online query pipelines  
- Works without real data (synthetic or public docs)  
- Section-level chunking + metadata ensures meaningful retrieval  
- Embedding model + FAISS chosen for simplicity, speed, and reproducibility  
- Fully extensible: future scaling, reranking, hybrid search, real docs  

---
