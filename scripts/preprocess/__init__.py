"""
Preprocessing Package

Main entry point for the document preprocessing pipeline.
"""

from pathlib import Path
from .preprocessing_pipeline import PreprocessingPipeline


def main():
    """Main entry point."""
    # Paths relative to project root
    script_dir = Path(__file__).parent.parent  # scripts/
    project_root = script_dir.parent
    
    data_dir = project_root / "data"
    chunks_dir = project_root / "chunks"
    
    # Run pipeline
    pipeline = PreprocessingPipeline(
        data_dir=str(data_dir),
        chunks_dir=str(chunks_dir),
        chunk_size=350,
        overlap=75
    )
    
    pipeline.run()


if __name__ == "__main__":
    main()
