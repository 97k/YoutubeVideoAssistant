from app.decorators import retry
from app import exceptions
import requests
from langchain.chains.summarize import load_summarize_chain
from ai import prompts
import functools
from langchain_core.runnables import RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from langchain_core.output_parsers import StrOutputParser
from app import settings


class AIHelper:
    def __init__(self) -> None:
        ...

    @staticmethod
    @retry(exit_if_not=exceptions.HuggingFaceInferenceException)
    def callmodel(model_id, input: str, temperature: float = 0.01, **kwargs):
        """
        Calls the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/en/quicktour)
        @param: model_id: The hugging face model to call
        @param: input: The input text to the model, you don't have to pass dictionary, this function will generate
        Make sure to pass kwargs supported by your model task type (eg: generation, summarisation)
        """
        headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
        params = {"temperature": temperature} | kwargs
        payload = {
            "inputs": input.strip(),
            "parameters": params,
            "options": {"wait_for_model": True, "use_cache": True},
        }

        response = requests.post(
            url := f"{settings.HF_INF_API}/{model_id}", headers=headers, json=payload
        )
        if response.status_code == 503:
            raise exceptions.HuggingFaceInferenceException(
                f"{response.status_code=:<10}|{response.text=}"
            )
        elif response.status_code in range(400, 410):
            raise requests.HTTPError(f"{response.status_code=} | {response.text=}")

        return response.json()


summary_chain = load_summarize_chain(
    llm=settings.llm,
    chain_type="map_reduce",
    verbose=True,
    combine_prompt=prompts.COMB_PROMPT,
)


@functools.cache
def rag_chain(user_message: str, retriever: BaseRetriever) -> str:
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompts.qa_prompt
        | settings.llm
        | StrOutputParser()
    )
    return rag_chain.invoke(f"{user_message}.")
