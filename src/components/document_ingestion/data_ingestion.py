from __future__ import annotations 
from pathlib import Path 
from typing import Iterable,List,Optional,Dict,Any 
import json 
import uuid 
from datetime import datetime
import hashlib 
import sys

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from src.utils.model_loader import ModelLoader 
from src.utils.file_io import save_uploaded_files
from src.utils.document_ops import load_documents
from src.logger.custom_logger import logger 
from src.exception.custom_exception import DocumentPortalException

def generate_session_id() -> str:
    """
    Generate a session folder (unique session id) with a timestamp
    it will create folders like
    data/
     session_abc/
        files
    faiss_index/
     session_abc/
        index.faiss 
        index.pkl 
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"

class ChatIngestor:
    def __init__(self,
                 temp_base: str = "data",
                 faiss_index: str = "faiss_index",
                 use_sessions_dirs: bool = True,
                 session_id: Optional[str] = None):
        try:
            self.model_loader = ModelLoader()
            self.use_session = use_sessions_dirs
            self.session_id = session_id or generate_session_id()

            self.temp_base = Path(temp_base)
            self.temp_base.mkdir(parents=True,exist_ok=True)

            self.faiss_base = Path(faiss_index)
            self.faiss_base.mkdir(parents=True,exist_ok=True)

            self.temp_dir = self._resolve_dir(self.temp_base)
            self.faiss_dir = self._resolve_dir(self.faiss_base)

            logger.info("Initialized ChatIngestor",
                        session_id=self.session_id,
                        temp_dir=str(self.temp_dir),
                        faiss_dir=str(self.faiss_dir),
                        sessionized=self.use_session)

        
        except Exception as e:
            logger.error("Failed to initialize ChatIngestor",error=str(e))
            raise DocumentPortalException(e,sys)

    def _resolve_dir(self,base: Path):
        if self.use_session:
            d = base / self.session_id 
            d.mkdir(parents=True,exist_ok=True)
            return d 
        return base 
    
    def _split(self,
                  docs:List[Document],
                  chunk_size=1000,
                  chunk_overlap=200) -> List[Document]:
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                  chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(docs)
        
        logger.info("Documents split",chunks=len(chunks),chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        return chunks  
    
    def _build_retriever(self,
                        uploaded_file: Iterable,
                        chunk_size: int = 1000,
                        chunk_overlap: int = 200,
                        k: int = 5,
                        search_type: str = "mmr",
                        fetch_k: int = 20,
                        lambda_mult: float = 0.5):
        try:
            paths = save_uploaded_files(uploaded_file,self.temp_dir)
            docs = load_documents(paths)

            if not docs:
                raise ValueError("No valid documents loaded")
            
            chunks = self._split(docs,
                                 chunk_size=chunk_size,
                                 chunk_overlap=chunk_overlap)
            
        except Exception as e:
            pass 


class FaissManager:
    def __init__(self,
                 index_dir: Path,
                 model_loader: Optional[ModelLoader]=None):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True,
                             exist_ok=True)
        
        self.meta_path = self.index_dir / "ingested_meta.json"
        self._meta: Dict[str, Any] = {"rows":{}}

        if self.meta_path.exists():
            try:
                self._meta = json.loads(self.meta_path.read_text(encoding="utf-8")) or {"rows":{}}
            except Exception:
                self._meta = {"rows":{}}

        self.model_loader = model_loader or ModelLoader() 
                                                                                                                                     