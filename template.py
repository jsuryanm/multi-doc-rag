import os 
from pathlib import Path
import logging 

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s]: %(message)s")

project_name = "multi_doc_chat"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/config/config.yaml",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/custom_exception.py",
    f"{project_name}/src/__init__.py",
    f"{project_name}/src/document_chat/__init__.py",
    f"{project_name}/src/document_chat/retrieval.py",
    f"{project_name}/src/document_ingestion/__init__.py",
    f"{project_name}/src/document_ingestion/data_ingestion.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/custom_logger.py",
    f"{project_name}/model/__init__.py",
    f"{project_name}/model/models.py",
    f"{project_name}/prompts/__init__.py",
    f"{project_name}/prompts/prompt_library.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/config_loader.py",
    f"{project_name}/utils/document_ops.py",
    f"{project_name}/utils/file_io.py",
    f"{project_name}/utils/model_loader.py",
    f"{project_name}/tests/conftest.py",
    f"{project_name}/tests/integration/__init__.py",
    f"{project_name}/tests/integration/test_chat_route.py",
    f"{project_name}/tests/integration/test_upload_route.py",
    f"{project_name}/tests/unit/test_data_ingestion.py",
    f"{project_name}/tests/unit/test_retrieval.py",
    "backend/__init__.py",
    "backend/app.py",
    "config/config.yaml",
    "data/AgenticAI.txt",
    "main.py",
    "Dockerfile.api",
    "Dockerfile.ui",
    ".dockerignore",
    "docker-compose.yml",
    "requirements.txt",
    "notebooks/experiments.ipynb",
    "notebooks/rag.ipynb",
    "notebooks/evaluation.ipynb",
    "streamlit_app.py",
    "run_evaluations.py",
    "test.py",
    ".env"
]

for file_path in list_of_files:
    file_path =  Path(file_path)
    file_dir,file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for file: {file_name}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path,"w") as f:
            pass
            logging.info(f"Creating an empty file: {file_path}")
    
    else:
        logging.info(f"{file_name} already exists")


