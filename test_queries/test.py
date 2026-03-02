import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# -----------------------------
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_DIR = os.path.join(PROJECT_DIR, "chunks/data")
INDEX_PATH = os.path.join(PROJECT_DIR, "index", "faiss_index.bin")
INDEX_JSON_PATH = os.path.join(PROJECT_DIR, "embeddings", "index.json")
MODEL_CACHE_DIR = os.path.join(PROJECT_DIR, "models_cache")
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = MODEL_CACHE_DIR

# -----------------------------
print("🔹 Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)
print(f"✅ Index loaded. Dimension: {index.d}, Num vectors: {index.ntotal}")

print("🔹 Loading index metadata...")
with open(INDEX_JSON_PATH, "r") as f:
    index_mapping = json.load(f)
print(f"✅ Loaded {len(index_mapping)} metadata entries")

# -----------------------------
print(f"🔹 Loading SentenceTransformer model '{MODEL_NAME}'...")
model = SentenceTransformer(MODEL_NAME)
print("✅ Model loaded")

# -----------------------------
# Create robust inverse index
inv_index = {}
for chunk_id, metadata in index_mapping.items():
    if isinstance(metadata, dict) and "index" in metadata:
        inv_index[metadata["index"]] = chunk_id
    elif isinstance(metadata, int):
        inv_index[metadata] = str(chunk_id)
    else:
        try:
            idx = int(chunk_id)
            inv_index[idx] = chunk_id
        except ValueError:
            continue

# -----------------------------
def search_query(query: str, top_k: int = TOP_K):
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    if q_emb.shape[1] != index.d:
        raise ValueError(f"Query embedding dim {q_emb.shape[1]} != index dim {index.d}")

    distances, indices = index.search(q_emb, top_k)
    
    results = []
    print(f"🔹 Search results for query: '{query}'")
    for dist, idx in zip(distances[0], indices[0]):
        chunk_id = inv_index.get(idx, None)
        if chunk_id:
            # safe source_file lookup
            metadata_entry = index_mapping.get(chunk_id, {})
            if isinstance(metadata_entry, dict):
                source_file = metadata_entry.get("source_file", "unknown")
            else:
                source_file = "unknown"

            # 🔹 Read chunk text from file
            chunk_path = os.path.join(CHUNKS_DIR, f'{chunk_id}.txt')
            if os.path.exists(chunk_path):
                with open(chunk_path, "r", encoding="utf-8") as f:
                    chunk_text = f.read()
            else:
                chunk_text = f'[Chunk text not found in {chunk_path}]'

            results.append({"chunk_id": chunk_id, "file": source_file, "score": float(dist), "text": chunk_text})
    return results

# -----------------------------
if __name__ == "__main__":
    print("\n💬 Enter your queries (type 'exit' to quit)")
    while True:
        query = input("Query> ").strip()
        if query.lower() in ("exit", "quit"):
            break
        try:
            print(f"🔹 Searching for: {query}")
            results = search_query(query)
            if not results:
                print("⚠️ No results found")
            else:
                print(f"✅ Top {len(results)} results:")
                for r in results:
                    print(f" - File: {r['file']}, text: {r['text'][:100]}..., Chunk: {r['chunk_id']}, Score: {r['score']:.4f}")
        except Exception as e:
            print(f"❌ Error: {e}")