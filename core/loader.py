from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

# TODO: Add PDF/HTML loader (e.g., PyPDFLoader, Unstructured, or custom)
def load_eu_ai_act(path: str) -> List[Dict[str, Any]]:
    """
    Loads and splits the EU AI Act document into chunks with metadata.
    Args:
        path: Path to the source document (PDF or HTML)
    Returns:
        List of dicts with 'text' and 'metadata'
    """
    # TODO: Load document from PDF/HTML
    raw_text = """PLACEHOLDER: Load the EU AI Act text here."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    chunks = splitter.split_text(raw_text)
    # TODO: Add real metadata (section, source, chunk_id)
    docs = [
        {"text": chunk, "metadata": {"section": "TODO", "source": path, "chunk_id": i}}
        for i, chunk in enumerate(chunks)
    ]
    return docs 