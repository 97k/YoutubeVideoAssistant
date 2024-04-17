import streamlit as st

st.set_page_config(
    page_title="Revisit Youtube Video Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from app import settings, Models
from app import data, Youtube
from app.logger import get_logger
import helpers
from ai.models import rag_chain
import asyncio

logger = get_logger(__name__)


def display_messages():
    if "rag_messages" in st.session_state:
        with infocol1:
            for msg in st.session_state["rag_messages"]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])


@st.cache_resource
def video_setup(video_url: str):
    logger.info(f"{video_url=}")

    st.write("Fetching Transcript...")
    yt = Youtube.from_video_url(video_url=video_url, process=False)
    # for qa 1 min and for summary, window of 4min
    st.session_state["summary"] = asyncio.run(yt.summarize())
    st.info("Summary Generated", icon="🌟")
    display_messages()
    st.write("Ingesting Data...")
    asyncio.run(yt.load_in_chroma())
    st.info("Data Ingested", icon="✅")

    return yt


st.write("# Revisit: Youtube Video assistant")
st.write(
    (
        "This project makes use of HuggingFaceInference API. "
        "If you're getting HTTP 424 or 500 erros, plese open sidebar and set your HuggingFace API Key. "
        "To generate, API keys [follow this](https://huggingface.co/docs/api-inference/en/quicktour)"
    )
)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

with st.sidebar:
    HF_API_TOKEN = st.text_input("HuggingFace API Key", type="password")
    st.write("[Star the code on github](https://github.com/97k/yt_qa_n_summary)")
    logger.info(f"{HF_API_TOKEN=}")
    if HF_API_TOKEN != "":
        settings.HF_TOKEN = HF_API_TOKEN


yt_vid = st.text_input("Paste youtube video URL")
infocol1, infocol2 = st.columns([4, 1])

with infocol2:
    llm = st.selectbox(label="Choose OS LLM", options=list(Models))
    logger.info(f"llm chosen: {llm}")
    if llm is not None:
        with st.status("Setting up LLM", expanded=False) as status:
            helpers.set_configs(llm=llm)
        status.update(label=f"LLM set to {llm}", state="complete")
    if yt_vid and yt_vid != "":
        yt = video_setup(yt_vid)

with infocol1:
    if yt_vid is None or yt_vid == "":
        st.info(body="Please insert youtube video url to continue", icon="🚨")
    else:
        if "summary" in st.session_state and st.session_state["summary"] is not None:
            st.write("## Summary of the video")
            st.write(st.session_state["summary"])

if yt_vid and yt.retriever is not None:
    input_text = st.chat_input(placeholder="Ask questions regarding this video")
    if "rag_messages" not in st.session_state:
        st.session_state["rag_messages"] = [
            {
                "role": "ai",
                "content": "hey There, hit me up with any questions related to the passed video",
            }
        ]
    if input_text is not None:
        st.session_state.rag_messages.append({"role": "user", "content": input_text})
        answer = rag_chain(input_text, retriever=yt.retriever)
        st.session_state.rag_messages.append({"role": "ai", "content": answer})


display_messages()
