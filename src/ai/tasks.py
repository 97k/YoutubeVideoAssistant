from ai.models import AIHelper
from app import settings
from app import exceptions
import pandas as pd
from typing import Literal


class LLMTasks:
    def __init__(self) -> None:
        ...

    @staticmethod
    async def generate_summary(text: str):
        return Rag.callmodel(model_id=settings.HF_SUMMARISER, input=text)

    # @staticmethod
    # def run_through_pandas(df: pd.DataFrame|pd.Series, task: Literal['summarisation', 'embed'], column: str | None = None):
    #     match task:
    #         case "summarisation":
    #             if type(df) == pd.Series:
    #                 return await df.apply(LLMTasks.generate_summary)
    #             elif type(df) == pd.DataFrame and column is not None:
    #                 return await df[column].apply(LLMTasks.generate_summary)
    #             raise exceptions.LLMTasksPandasError(f"Either pass a single column, or if passing dataframe please pass `column` to choose from")
    #         case "embed":
    #             ...
    #     return True


from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=80, length_function=len
)


def get_docs_from_df(df: pd.DataFrame, text_splitter=text_splitter):
    """Return Youtube resampled Df{text, custom_url} in documents with metadata"""
    docs = []
    for idx, row in tqdm(df.iterrows()):
        text, source = row["text"], row["custom_url"]
        if len(text) > text_splitter._chunk_size:
            split_docs = text_splitter.create_documents([text])
            for doc in split_docs:
                doc.metadata = {"source": source}
                docs.append(doc)
        else:
            doc = Document(page_content=text, metadata={"source": source})
            docs.append(doc)

    return docs
