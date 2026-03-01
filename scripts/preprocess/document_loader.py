"""
Document Loader — Loads documents from various formats.

Supports:
- Markdown (.md)
- Plain text (.txt)
- HTML (extensible)
"""

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Document:
    doc_id: str
    content: str
    source: str
    format: str


class DocumentLoader:
    """Load documents from various formats (Markdown, HTML, plain text)."""
    
    data_dir: Path
    documents: List[Dict] 

    def __init__(self, data_dir: str):
        """Initialize with data directory path."""
        self.data_dir = Path(data_dir)
        self.documents = []
    
    def load_markdown(self, file_path: str) -> Document:
        """
        Load a Markdown file and extract content.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Dict with doc_id, content, and metadata
        """
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with p.open('r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 decoding fails
            try:
                with p.open('r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read {file_path}: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to read {file_path}: {e}") from e

        doc_id = p.stem

        return Document(
            doc_id=doc_id,
            content=content,
            source=str(p),
            format='markdown'
        )
    
    def load_text(self, file_path: str) -> Document:
        """
        Load a plain text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Dict with doc_id, content, and metadata
        """
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with p.open('r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 decoding fails
            try:
                with p.open('r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read {file_path}: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to read {file_path}: {e}") from e

        doc_id = p.stem

        return Document(
            doc_id=doc_id,
            content=content,
            source=str(p),
            format='text'
        )
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all documents from data directory.
        
        Supports: .md, .txt, .markdown files
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        if not self.data_dir.exists():
            print(f"⚠️  Data directory not found: {self.data_dir}")
            return documents
        
        # Find all markdown and text files
        for file_path in self.data_dir.glob('**/*.md'):
            try:
                doc = self.load_markdown(str(file_path))
                documents.append(doc)
                print(f"✓ Loaded: {file_path}")
            except Exception as e:
                print(f"✗ Error loading {file_path}: {e}")
        
        for file_path in self.data_dir.glob('**/*.txt'):
            try:
                doc = self.load_text(str(file_path))
                documents.append(doc)
                print(f"✓ Loaded: {file_path}")
            except Exception as e:
                print(f"✗ Error loading {file_path}: {e}")
        
        self.documents = documents
        return documents
