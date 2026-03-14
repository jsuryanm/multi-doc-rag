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
from src.logger.custom_logger import logger 
from src.exception.custom_exception import DocumentPortalException

def generate_session_id() -> str:
    """Generate a unique session id with a timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"

