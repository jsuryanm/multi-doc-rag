from pydantic import BaseModel


class HuggingFaceEmbeddingConfig(BaseModel):
    model_name: str


class OpenAIEmbeddingConfig(BaseModel):
    model_name: str


class EmbeddingConfig(BaseModel):
    active_provider: str
    huggingface: HuggingFaceEmbeddingConfig
    openai: OpenAIEmbeddingConfig


class RetrieverConfig(BaseModel):
    top_k: int
    search_type: str
    fetch_k: int
    lambda_mult: float


class LLMProviderConfig(BaseModel):
    provider: str
    model_name: str
    temperature: float
    max_output_tokens: int


class LLMConfig(BaseModel):
    active_provider: str
    groq: LLMProviderConfig
    openai: LLMProviderConfig


class AppConfig(BaseModel):
    embedding_model: EmbeddingConfig
    retriever: RetrieverConfig
    llm: LLMConfig