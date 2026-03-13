import os 
import sys 
import json 
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from src.utils.config_loader import load_config
from src.logger.custom_logger import logger 
from src.exception.custom_exception import DocumentPortalException


class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY","OPENAI_API_KEY"]

    def __init__(self):
        self.api_keys = {}

        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)

                if env_val:
                    self.api_keys[key] = env_val
                    logger.info(f"Loaded {key} from individual environment variable")
        
        missing_keys = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing_keys:
            logger.error("Missing API keys",missing_keys=missing_keys)
            raise DocumentPortalException("Missing API keys",sys)
        
        logger.info("API keys loaded",keys={key:val[:6] + "..." for key,val in self.api_keys.items()})

    def get(self,key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val 
    
class ModelLoader:
    pass