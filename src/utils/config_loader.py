import os 
import yaml 
import sys
from pathlib import Path 

from src.logger.custom_logger import logger 
from src.exception.custom_exception import DocumentPortalException
from src.entity.config_entity import AppConfig

def _package_root() -> Path:
    """
    This function returns the package root of project
    dir sturcture muti_doc_rag/src/utils/config_loader.py
    returns: src
    """

    return Path(__file__).resolve().parents[1]


def load_config(config_path: str | None = None) -> dict:
    """
    Resolve config path reliably irrespective of CWD.
    Priority: explicit arg > CONFIG_PATH env > <project_root>/config/config.yaml
    """
    try:
        env_path = os.getenv("CONFIG_PATH")

        if config_path is None:
            config_path = env_path or str(_package_root() / "config" / "config.yaml")
            
        path = Path(config_path)

        if not path.is_absolute():
            path = _package_root() / path

        if not path.exists():
            raise DocumentPortalException(f"Config file not found: {path}",sys) 
        
        with open(path,"r",encoding="utf-8") as f:
            logger.info("loading config.yaml")
            data = yaml.safe_load(f)

            if data is None:
                raise DocumentPortalException("Config file is empty",sys)

            config = AppConfig(**data)
            return config
        
    except Exception as e:
        logger.error("Config loading failed",error=str(e))
        raise DocumentPortalException(e,sys)


# if __name__ == "__main__":
#     load_config()