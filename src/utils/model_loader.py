import os 
import sys 
import json 
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

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
    """Loads embedding models and LLM's based on config anf environment"""

    def __init__(self):
        if os.getenv("ENV","local").lower() != "production":
            load_dotenv()
            logger.info("Running in local mode, Loading .env file")
        else:
            logger.info("Running in production mode")
        
        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()
        logger.info("YAML config loaded",config_keys=list(self.config.model_dump().keys()))

    
    def load_embeddings(self):
        """Load and return the embeddings model from HuggingFace"""
        try:
                
            provider = self.config.embedding_model.active_provider
            
            if provider == "huggingface":
                hf_embeddings = HuggingFaceEmbeddings(model_name=self.config.embedding_model.huggingface.model_name)
                logger.info("Loading HuggingFaceEmbeddings")
                return hf_embeddings
            
            elif provider == "openai":
                openai_embeddings = OpenAIEmbeddings(model_name=self.config.embedding_model.openai.model_name)
                logger.info("Loading OpenAIEmbeddings")
                return openai_embeddings
        
        except Exception as e:
            logger.error("Error loading embeddings model",error=str(e))
            raise DocumentPortalException("Failed to load embeddings model",sys)
        
    def load_llm(self):
        """
        Load and return the configured LLM model
        """
        llm_block = self.config.llm
        provider_key = llm_block.active_provider

        if not hasattr(llm_block,provider_key):
            logger.error("LLM provider not found in config",provider=provider_key)
            raise ValueError(f"LLM provider {provider_key} not found in config")
        
        llm_config = getattr(llm_block,provider_key)

        provider = llm_config.provider
        model_name = llm_config.model_name
        temperature = llm_config.temperature
        max_tokens = llm_config.max_output_tokens

        logger.info("Loading LLM",provider=provider,model=model_name)

        if provider == "openai":
            return ChatOpenAI(model=model_name,
                              api_key=self.api_key_mgr.get("OPENAI_API_KEY"),
                              temperature=temperature,
                              max_completion_tokens=max_tokens)
        
        elif provider == "groq":
            return ChatGroq(model=model_name,
                            api_key=self.api_key_mgr.get("GROQ_API_KEY"),
                            temperature=temperature)

if __name__ == "__main__":
    loader = ModelLoader()

    embeddings = loader.load_embeddings()
    print("Embedding models loaded:",embeddings)
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embeddings result: {result}")

    llm = loader.load_llm()
    print(f"LLM loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM result: {result.content}")