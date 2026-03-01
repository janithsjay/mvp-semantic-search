# MVP Semantic Search — Full Setup & Technical Instructions

This document contains all the details for setting up, managing, and understanding the **retrieval-only semantic search MVP** using Python, FAISS, and pre-trained embeddings.

---

## 1️⃣ Project Overview

This MVP focuses on **retrieving relevant sections from technical documentation** using pre-trained embeddings without any fine-tuning.

**Key Components:**

* Document Loader & Chunking (sections + token overlap)
* Embedding Layer (bi-encoder transformer)
* FAISS Vector Index (similarity search)
* Metadata Storage (JSON/SQLite)
* Query Pipeline (embedding query → FAISS search → return text + metadata)

---

## 2️⃣ Folder Structure

```
mvp-semantic-search/
├── data/                  # Raw documents (Markdown/HTML/synthetic)
├── chunks/                # Section-level chunks + metadata
├── embeddings/            # Serialized embeddings (.npy, .pt)
├── index/                 # FAISS index files (.bin)
├── scripts/               # Pipeline & venv management scripts
│   └── manage_venv.sh     # Setup / activate / deactivate venv
├── test_queries/          # Test/evaluation queries
├── TECH_SELECTIONS.md     # Technical selections details
├── SI.md                  # Solution Intent
├── ARCHITECTURE.md        # System architecture diagrams
├── README.md              # Repo overview & usage
├── INSTRUCTIONS.md        # This file
├── requirements.txt       # Python dependencies
└── .gitignore
```

> The structure separates raw data, processed chunks, embeddings, and scripts to keep things modular and scalable.

---

## 3️⃣ Python Virtual Environment

We use a **project-specific virtual environment**:

```bash
venv_mvp_semsearch
```

**Benefits:**

* Isolation from the host Python environment
* Reproducibility
* Safety: prevents conflicts with other projects

### 3.1 Single Management Script

All venv tasks are handled by:

```bash
scripts/manage_venv.sh
```

**Usage:**

```bash
# Setup environment + install dependencies
./manage_venv.sh setup

# Activate venv
./manage_venv.sh activate

# Deactivate venv
./manage_venv.sh deactivate
```

---

## 4️⃣ Python Dependencies

All dependencies are listed in `requirements.txt`:

```text
sentence-transformers==2.2.2
faiss-cpu==1.7.4
numpy==1.25.0
nltk==3.8.1
spacy==3.6.0
```

**Purpose:**

| Package               | Role                                          |
| --------------------- | --------------------------------------------- |
| sentence-transformers | Generate embeddings for documents and queries |
| faiss-cpu             | Vector similarity search                      |
| numpy                 | Numerical operations                          |
| nltk / spacy          | Tokenization, chunking                        |

> Versions are pinned for reproducibility.

---

## 5️⃣ Technical Selections

**Document Loader:** Python scripts using `markdown` or `BeautifulSoup` — handles multiple formats, preprocessing, and cleaning.

**Chunking Layer:** Section + token-based chunks (300–400 tokens, 50–100 overlap) — preserves semantic context, prevents info loss at boundaries.

**Embedding Model:** `all-MiniLM-L6-v2` (Sentence Transformers)

* Bi-encoder transformer, L2-normalized vectors
* Lightweight, CPU-friendly, pretrained
* Future upgrades: `all-mpnet-base-v2`, `bge-base-en-v1.5`

**Vector Index:** FAISS (`IndexFlatIP`)

* Efficient similarity search for dense vectors
* Lightweight, serialized to disk for offline/online pipelines

**Metadata Storage:** JSON or SQLite

* Maps `vector_id → chunk text + metadata`
* Lightweight, portable, and easy to update

**Query Pipeline:** Python script

* Embed query with same model + normalization
* Perform top-K search in FAISS
* Return text + metadata

**Evaluation / Testing:** Small synthetic query set, metrics: Recall@K, MRR

---

## 6️⃣ Setting Up the Environment

1. Clone the repo:

```bash
git clone https://github.com/yourusername/mvp-semantic-search.git
cd mvp-semantic-search/scripts
```

2. Setup virtual environment + install dependencies:

```bash
./manage_venv.sh setup
```

3. Activate the environment:

```bash
./manage_venv.sh activate
```

4. Deactivate the environment when done:

```bash
./manage_venv.sh deactivate
```

---

## 7️⃣ Example Workflow for MVP

```bash
# Setup environment
./manage_venv.sh setup

# Activate environment
./manage_venv.sh activate

# Run preprocessing (document loader + chunking)
python preprocess.py

# Generate embeddings
python embed.py

# Build FAISS index
python build_index.py

# Query the system
python query_index.py

# Deactivate environment
./manage_venv.sh deactivate
```

---

## 8️⃣ Notes & Best Practices

* Always activate venv before running any scripts
* FAISS index, embeddings, and processed chunks are **not tracked by Git**
* This setup is for **MVP development only**; Docker can be introduced later if:

  * Vector DB (Milvus, Weaviate) is needed
  * Metadata DB (PostgreSQL, SQLite) is needed
  * REST API / multi-user access is required

---

## 9️⃣ References & Further Considerations

* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Sentence Transformers: [https://www.sbert.net/](https://www.sbert.net/)
* Tokenization & NLP: [https://spacy.io/](https://spacy.io/)
* MVP is designed to be **modular, scalable, and production-aware**, allowing easy upgrades to full vector DBs or cloud deployments in the future.
