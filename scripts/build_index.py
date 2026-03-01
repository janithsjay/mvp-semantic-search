"""
build_index.py

Build FAISS index for MVP Semantic Search project.

Reads embeddings from embeddings.npy and chunk IDs from index.json,
builds a FAISS index, and saves the index + metadata to index/.
"""

import os
import json
import numpy as np
import faiss

# --- Paths ---
EMBEDDINGS_DIR = "../embeddings"  # adjust if running from scripts/
EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, "embeddings.npy")
INDEX_JSON_FILE = os.path.join(EMBEDDINGS_DIR, "index.json")

INDEX_DIR = "../index"
INDEX_PATH = os.path.join(INDEX_DIR, "faiss_index.bin")
CHUNK_META_PATH = os.path.join(INDEX_DIR, "chunk_metadata.json")

# --- Prepare index directory ---
os.makedirs(INDEX_DIR, exist_ok=True)

# --- Load embeddings ---
embeddings_matrix = np.load(EMBEDDINGS_FILE).astype("float32")
print(f"Loaded embeddings: {embeddings_matrix.shape}")

# --- Load chunk IDs ---
with open(INDEX_JSON_FILE, "r") as f:
    chunk_id_map = json.load(f)  # {chunk_id: row_index}

# --- Build metadata list ---
# We'll store chunk_id only for now; text can be linked later
chunk_metadata = [{"chunk_id": k, "row_index": v} for k, v in chunk_id_map.items()]

# --- Normalize embeddings for cosine similarity ---
faiss.normalize_L2(embeddings_matrix)

# --- Create FAISS index ---
dim = embeddings_matrix.shape[1]
index = faiss.IndexFlatIP(dim)  # Inner-product similarity
index.add(embeddings_matrix)
print(f"FAISS index created with {index.ntotal} vectors.")

# --- Save FAISS index ---
faiss.write_index(index, INDEX_PATH)
print(f"FAISS index saved to {INDEX_PATH}")

# --- Save chunk metadata ---
with open(CHUNK_META_PATH, "w") as f:
    json.dump(chunk_metadata, f, indent=2)
print(f"Chunk metadata saved to {CHUNK_META_PATH}")