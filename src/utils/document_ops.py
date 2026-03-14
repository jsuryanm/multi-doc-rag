from __future__ import annotations
from pathlib import Path
from typing import Iterable, Union,List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from src.logger.custom_logger import logger 
from src.exception.custom_exception import DocumentPortalException
from fastapi import UploadFile
import os 
import sys 

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def load_documents(paths: Union[Iterable[Path]]) -> List[Document]:
    """Load docs using appropriate loader based on extension."""
    if isinstance(paths,(str,Path)):
        paths = [Path(paths)]

    docs: List[Document] = []
    try:
        for p in paths:
            p = Path(p)
            ext = p.suffix.lower()
            if ext == ".pdf":
                loader = PyPDFLoader(str(p))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(p))
            elif ext == ".txt":
                loader = TextLoader(str(p), encoding="utf-8")
            else:
                logger.warning("Unsupported extension skipped", path=str(p))
                continue
            docs.extend(loader.load())
        logger.info("Documents loaded", count=len(docs))
        return docs
    
    except Exception as e:
        logger.error("Failed loading documents", error=str(e))
        raise DocumentPortalException(e,sys)
    

class FastAPIFileAdapter:
    """Adapt FastAPI UploadFile to a simple object with .name and .getbuffer()."""
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename or "file"

    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()
    

# if __name__ == "__main__":
#     DATA_PATH = os.path.join("data")
#     load_documents(DATA_PATH)