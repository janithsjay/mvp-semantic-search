"""
Preprocessing Pipeline — Orchestrates the complete preprocessing workflow.

Workflow:
1. Load documents from data/ directory
2. Extract sections from documents
3. Chunk sections into overlapping chunks
4. Save chunks and metadata
"""

import json
from pathlib import Path
from typing import List

from preprocess.document_loader import DocumentLoader, Document
from preprocess.document_chunker import DocumentChunker, Chunk
from dataclasses import asdict


class PreprocessingPipeline:
    """Complete preprocessing pipeline: load → extract → chunk → save."""
    
    def __init__(self, data_dir: str, chunks_dir: str, chunk_size: int = 350, overlap: int = 75):
        """
        Initialize pipeline.
        
        Args:
            data_dir: Input data directory
            chunks_dir: Output chunks directory
            chunk_size: Target tokens per chunk
            overlap: Overlap tokens
        """
        self.data_dir = data_dir
        self.chunks_dir = Path(chunks_dir)
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        
        self.loader = DocumentLoader(data_dir)
        self.chunker = DocumentChunker(chunk_size=chunk_size, overlap=overlap)
    
    def run(self) -> None:
        """Execute the complete preprocessing pipeline."""
        print("=" * 60)
        print("MVP Semantic Search — Preprocessing Pipeline")
        print("=" * 60)
        
        # Step 1: Load documents
        print("\n[1/3] Loading documents...")
        documents: List[Document] = self.loader.load_all_documents()
        
        if not documents:
            print("⚠️  No documents found. Please add .md or .txt files to the data/ directory.")
            return
        
        print(f"✓ Loaded {len(documents)} document(s)")
        
        # Step 2: Chunk documents
        print("\n[2/3] Chunking documents...")
        all_chunks: List[Chunk] = []
        for doc in documents:
            chunks = self.chunker.chunk_document(doc)
            all_chunks.extend(chunks)
            print(f"  → {doc.doc_id}: {len(chunks)} chunks")
        
        print(f"✓ Created {len(all_chunks)} total chunks")
        
        # Step 3: Save chunks and metadata
        print("\n[3/3] Saving chunks and metadata...")
        
        # Save individual chunk files
        chunks_data_dir = self.chunks_dir / "data"
        chunks_data_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_list = []
        for chunk in all_chunks:
            # Save chunk content
            chunk_file = chunks_data_dir / f"{chunk.chunk_id}.txt"
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk.content)
            
            # Prepare metadata (exclude content)
            meta = asdict(chunk)
            meta.pop('content', None)
            metadata_list.append(meta)
        
        # Save metadata index
        metadata_file = self.chunks_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, indent=2)
        
        print(f"✓ Saved {len(all_chunks)} chunks to {chunks_data_dir}")
        print(f"✓ Saved metadata to {metadata_file}")
        
        # Summary statistics
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Documents processed: {len(documents)}")
        print(f"Total chunks created: {len(all_chunks)}")
        avg_tokens = sum(c.token_count for c in all_chunks) / len(all_chunks) if all_chunks else 0
        print(f"Average tokens per chunk: {avg_tokens:.1f}")
        print(f"Chunk size target: {self.chunker.chunk_size} (±100)")
        print(f"Chunk overlap: {self.chunker.overlap} tokens")
        print("=" * 60)
