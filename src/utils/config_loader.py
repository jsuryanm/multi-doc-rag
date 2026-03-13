from pathlib import Path 
import os 
import yaml 
from src.logger.custom_logger import logger 

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
    env_path = os.getenv("CONFIG_PATH")

    if config_path is None:
        config_path = env_path or str(_package_root() / "config" / "config.yaml")
        
    path = Path(config_path)

    if not path.is_absolute():
        path = _package_root() / path

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}") 
    
    with open(path,"r",encoding="utf-8") as f:
        logger.info("loading config.yaml")
        return yaml.safe_load(f) or f


# if __name__ == "__main__":
#     load_config()