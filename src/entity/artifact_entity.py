from pydantic import BaseModel 
from pathlib import Path 

class DataIngestionArtifact(BaseModel):
    raw_data_path: Path
    processed_data_path: Path 

class EmbeddingsArtifact(BaseModel):
    vector_store_path: Path
    embeddings_model: str

class RetrieverArtifact(BaseModel):
    retriever_doc_counts: int
    search_type: str

class RAGArtifact(BaseModel):
    prompt_tokens: int 
    completion_tokens: int 
    total_tokens: int 