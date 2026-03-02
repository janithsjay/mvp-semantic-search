import os
import json
import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_DIR = os.path.join(PROJECT_DIR, "chunks/data/")
INDEX_PATH = os.path.join(PROJECT_DIR, "index", "faiss_index.bin")  # Path to your FAISS index
MAPPING_PATH = os.path.join(PROJECT_DIR, "index", "chunk_metadata.json")  # Your JSON mapping
TOP_K = 5

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# -----------------------------
# LOAD FAISS INDEX
# -----------------------------
@st.cache_resource
def load_index():
    if not os.path.exists(INDEX_PATH):
        return None
    return faiss.read_index(INDEX_PATH)

index = load_index()

# -----------------------------
# LOAD MAPPING
# -----------------------------
def load_mapping():
    if not os.path.exists(MAPPING_PATH):
        return []
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

index_mapping = load_mapping()

# Build inverse mapping (row_index -> chunk_id)
inv_index = {item["row_index"]: item["chunk_id"] for item in index_mapping}

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🔍 MVP Semantic Search")
st.write(f"Indexed vectors: {index.ntotal if index else 0}")

if index is None:
    st.error("FAISS index not found. Please run preprocessing + indexing first.")
    st.stop()

with st.form("search_form"):
    query = st.text_input("Enter your query:")
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    st.write(f"🔎 Searching for: `{query}`")

    # Encode query
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")

    # Search
    distances, indices = index.search(q_emb, TOP_K)

    st.subheader("Results")

    found = False

    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        chunk_id = inv_index.get(idx)
        if not chunk_id:
            continue

        found = True

        # Read chunk text
        chunk_file = f"{chunk_id}.txt"
        chunk_path = os.path.join(CHUNKS_DIR, chunk_file)

        chunk_text = ""
        if os.path.exists(chunk_path):
            with open(chunk_path, "r", encoding="utf-8") as f:
                chunk_text = f.read()
        else:
            chunk_text = f"⚠️ Chunk file not found: {chunk_path}"

        # Display result
        with st.expander(f"📄 {chunk_file} | Score: {dist:.4f}"):
            st.write(chunk_text)

    if not found:
        st.warning("⚠️ No results found.")