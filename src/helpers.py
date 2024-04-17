from app import settings, Models
from langchain.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
import streamlit as st


@st.cache_data
def set_configs(llm: Models, embedding_model="intfloat/multilingual-e5-large-instruct"):
    """Update the settings to use specifc llm"""
    hf_embed = HuggingFaceInferenceAPIEmbeddings(
        api_key=settings.HF_TOKEN,
        model_name=(HF_EMBED_MODEL_ID := "intfloat/multilingual-e5-large-instruct"),
    )
    llm = HuggingFaceEndpoint(repo_id=llm, huggingfacehub_api_token=settings.HF_TOKEN)
    settings.embed_model = hf_embed
    settings.llm = llm
    return True
