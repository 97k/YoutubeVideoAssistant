from typing import Optional
from langchain_core.language_models.llms import LLM
from langchain_core.embeddings import Embeddings

from langchain import pydantic_v1 as pyd
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from enum import Enum


class Models(str, Enum):
    MIXTRAL_8_7B_INSTRUCT: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    ZEPHYR_7B_BETA: str = "HuggingFaceH4/zephyr-7b-beta"
    MISTRAL_7B_INSTRUCT_VPOINT2: str = "mistralai/mistral-7b-instruct-v0.2"


class Settings(pyd.BaseSettings):
    HF_TOKEN: str
    HF_INF_API: pyd.AnyUrl = (
        "https://api-inference.huggingface.co/models"  # to support any TGI hosted API
    )
    llm: Optional[LLM] = None
    embed_model: Optional[Embeddings] = None
    summarizer_model: Optional[str] = None

    class Config:
        extra = "allow"
        validate_assignment = True
