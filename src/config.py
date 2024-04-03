import langchain.pydantic_v1 as pyd


class Settings(pyd.BaseSettings):
    HF_TOKEN: str
    HF_INF_API: pyd.AnyUrl = (
        "https://api-inference.huggingface.co/models"  # to support any TGI hosted API
    )


settings = Settings()
