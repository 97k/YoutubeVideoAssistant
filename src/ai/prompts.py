## combine prompt
from langchain_core.prompts import PromptTemplate

comb_prompt = """You are a helpful assistant who is given with list of summaries of transcripts below. Your goal is to write a joined summary that highlights key points discussed in the video.
Do not respond with anything outside of the transcript. If you don't know answer, sorry, I can't do this right now.

You MUST Respond in the following format
     - A few short paragragaphs
     - Do not go longer than 4 sentences per paragraph

"{text}"
SUMMARY:
"""
COMB_PROMPT = PromptTemplate(template=comb_prompt, input_variables=["text"])


qa_prompt = """You are a helpful assistant, for question answering task. Only use the provided context to answer the question. If you don't know the answer, just say that you don't know. Use three sentence maxium and keep the answer concise.
If you are able to answer the question with provided context, Make sure you return the `custom_url` with your answer, This will be available in the metadata with source field.
Do not make up any other data from yourself, if you are not able to answer the question it is fine. If the provided context doesn't have answer to the user question, just tell user that "This video won't address your question, and my expertise is limited to providing context within its content only."`

Question: {question}
Context: {context}
Answer:
"""
qa_prompt = PromptTemplate(template=qa_prompt, input_variables=["question", "context"])
