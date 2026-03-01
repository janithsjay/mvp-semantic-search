import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# -----------------------------
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
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
def search_query(query: str, top_k: int = TOP_K):
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    if q_emb.shape[1] != index.d:
        raise ValueError(f"Query embedding dim {q_emb.shape[1]} != index dim {index.d}")

    distances, indices = index.search(q_emb, top_k)
    # invert index
    inv_index = {v["index"]: k for k, v in index_mapping.items()}

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        chunk_id = inv_index.get(idx, None)
        if chunk_id:
            source_file = index_mapping[chunk_id]["source_file"]
            results.append({"chunk_id": chunk_id, "file": source_file, "score": float(dist)})
    return results

# -----------------------------
if __name__ == "__main__":
    print("\n💬 Enter your queries (type 'exit' to quit)")
    while True:
        query = input("Query> ").strip()
        if query.lower() in ("exit", "quit"):
            break
        try:
            results = search_query(query)
            if not results:
                print("⚠️ No results found")
            else:
                for r in results:
                    print(f" - File: {r['file']}, Chunk: {r['chunk_id']}, Score: {r['score']:.4f}")
        except Exception as e:
            print(f"❌ Error: {e}")