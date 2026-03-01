"""
Document Chunker — Chunks documents into sections with token-based overlap.

Chunk Strategy:
- Size: 300–400 tokens per chunk
- Overlap: 50–100 tokens
- Preserve: Headings, code blocks, metadata
"""

import re
from typing import List, Tuple
from dataclasses import dataclass

from langchain.text_splitter import TokenTextSplitter

from .document_loader import Document

@dataclass
class Section:
    title: str
    content: str
    level: int

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    section_title: str
    section_index: int
    chunk_index: int
    content: str
    token_count: int


class DocumentChunker:
    """
    Chunk documents into sections with token-based overlap.
    """

    def __init__(self, chunk_size: int = 350, overlap: int = 75, encoding_name: str = "gpt2"):
        self.chunk_size = chunk_size
        self.overlap = overlap
        # TokenTextSplitter will handle both chunk sizing and overlap
        self.splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            encoding_name=encoding_name,
        )

    def count_tokens(self, text: str) -> int:
        # basic whitespace-based count; can be replaced by something
        # more accurate (e.g. tiktoken) if desired
        return len(text.split())

    def extract_sections(self, content: str) -> List[Section]:
        sections: List[Section] = []
        lines = content.split('\n')

        current_section = ""
        current_title = "Introduction"
        current_level = 0

        for line in lines:
            heading_match = re.match(r'^(#+)\s+(.+)$', line)
            if heading_match:
                if current_section.strip():
                    sections.append(Section(title=current_title,
                                            content=current_section.strip(),
                                            level=current_level))
                current_level = len(heading_match.group(1))
                current_title = heading_match.group(2).strip()
                current_section = f"# {current_title}\n"
            else:
                current_section += line + "\n"

        if current_section.strip():
            sections.append(Section(title=current_title,
                                    content=current_section.strip(),
                                    level=current_level))

        return sections

    def chunk_section(self, section_title: str, section_content: str, doc_id: str, section_index: int) -> List[Chunk]:
        # use the LangChain splitter to produce chunk texts
        texts = self.splitter.split_text(section_content)
        chunks: List[Chunk] = []
        for idx, text in enumerate(texts):
            chunks.append(Chunk(
                chunk_id=f"{doc_id}_s{section_index}_c{idx}",
                doc_id=doc_id,
                section_title=section_title,
                section_index=section_index,
                chunk_index=idx,
                content=text,
                token_count=self.count_tokens(text),
            ))
        return chunks

    def chunk_document(self, document: Document) -> List[Chunk]:
        doc_id = document.doc_id
        content = document.content

        sections = self.extract_sections(content)
        if not sections:
            sections = [Section(title="Full Document", content=content, level=0)]

        all_chunks: List[Chunk] = []
        for idx, section in enumerate(sections):
            section_chunks = self.chunk_section(section.title, section.content, doc_id, idx)
            all_chunks.extend(section_chunks)

        return all_chunks
