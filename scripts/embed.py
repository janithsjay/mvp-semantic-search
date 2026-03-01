"""
Generate and serialize embeddings for all chunks produced by the preprocessing
pipeline.

Usage:
    python scripts/embed.py [--model MODEL_NAME]

The script performs the following steps:
1. Load chunk metadata from `chunks/metadata.json`.
2. Read each chunk's text file from `chunks/data/`.
3. Embed texts using a SentenceTransformer model (default `all-MiniLM-L6-v2`).
4. Normalize vectors (L2) and write a NumPy array to `embeddings/embeddings.npy`.
5. Save an index mapping (chunk_id -> position) to
   `embeddings/index.json` for later lookup.

The embeddings directory is created if it doesn't already exist.
"""

import argparse
import json
from pathlib import Path
import numpy as np

from sentence_transformers import SentenceTransformer


def load_metadata(meta_path: Path):
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Embed preprocessed chunks.")
    parser.add_argument(
        "--model",
        type=str,
        default="all-MiniLM-L6-v2",
        help="SentenceTransformers model name",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    chunks_dir = project_root / "chunks"
    embeddings_dir = project_root / "embeddings"
    embeddings_dir.mkdir(parents=True, exist_ok=True)

    metadata_file = chunks_dir / "metadata.json"
    if not metadata_file.exists():
        print(f"Metadata file not found: {metadata_file}")
        return

    metadata = load_metadata(metadata_file)
    texts = []
    ids = []
    for entry in metadata:
        cid = entry["chunk_id"]
        chunk_file = chunks_dir / "data" / f"{cid}.txt"
        if not chunk_file.exists():
            print(f"Warning: chunk file missing {chunk_file}")
            texts.append("")
        else:
            texts.append(chunk_file.read_text(encoding='utf-8'))
        ids.append(cid)

    print(f"Embedding {len(texts)} chunks with model {args.model}...")
    model = SentenceTransformer(args.model)
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    # L2 normalize
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    vectors = vectors / norms

    out_path = embeddings_dir / "embeddings.npy"
    np.save(out_path, vectors)

    index_path = embeddings_dir / "index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump({cid: idx for idx, cid in enumerate(ids)}, f, indent=2)

    print(f"Saved embeddings to {out_path}")
    print(f"Saved index to {index_path}")


if __name__ == "__main__":
    main()
