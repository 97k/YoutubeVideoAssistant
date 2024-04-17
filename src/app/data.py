from utils import clean_text
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime as dt
from urllib.parse import urlparse, parse_qs
from ai.tasks import get_docs_from_df
from ai.models import summary_chain
from langchain_community.vectorstores.chroma import Chroma
from functools import lru_cache
from app.logger import get_logger
from app import settings

logger = get_logger(__name__)


class YoutubeWrapper:
    def __init__(
        self,
        video_url: str,
        transcript_data: pd.DataFrame,
        resampled_data: pd.DataFrame | None = None,
    ) -> None:
        self.video_url = video_url
        self.transcript_data = transcript_data
        self.resampled_data = resampled_data

    @staticmethod
    def get_yt_id(videourl: str):
        """Returns the Youtube Video-id from the youtube URL"""
        return parse_qs(urlparse(videourl).query).get("v")[0]

    @staticmethod
    def get_transcript(video_id: str, language: list = ["en"]):
        """Returns the transcript of a youtube video"""
        ts = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=language)
        return ts

    @classmethod
    def from_video_url(
        cls, video_url: str, window: str | None = "1min", process: bool = False
    ):
        # TODO: validate URL
        ts = cls.get_transcript(cls.get_yt_id(video_url))
        df = pd.DataFrame(ts)
        start = dt.datetime(year=2000, month=1, day=1)
        df.index = df["start"].apply(lambda x: dt.timedelta(seconds=x) + start)
        df["text"] = df["text"].apply(clean_text)
        df["text"] = df["text"] + " "
        if process:
            window = "30s" if window is None else window
            # df = cls.resample(video_url=video_url, transcript_data=df, window=window)
            obj = cls(video_url, df)
            resampled = obj.resample(window=window)
            return cls(video_url, df, resampled)
        return cls(video_url, df)

    @lru_cache
    def resample(self, window: str) -> pd.DataFrame:
        """Resamples a copy of dataframe on provided window"""
        df = self.transcript_data.copy(deep=True)
        df_text = (
            df[["text", "start", "duration"]]
            .resample(window)
            .agg({"text": sum, "start": list, "duration": "last"})
        )
        df_text["s"], df_text["e"] = zip(*df_text.start.apply(lambda x: (x[0], x[-1])))
        df_text["e"] += df_text["duration"]
        df_text["custom_url"] = (
            self.video_url
            + "&start="
            + df_text["s"].astype(int).astype(str)
            + "&end="
            + df_text["e"].astype(int).astype("str")
        )

        return df_text[["text", "custom_url"]]


class Youtube(YoutubeWrapper):
    def __init__(
        self,
        video_url: str,
        transcript_data: pd.DataFrame,
        resampled_data: pd.DataFrame | None = None,
    ) -> None:
        super().__init__(video_url, transcript_data, resampled_data)
        self._summary = None
        self._retriever = None

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value: str):
        self._summary = value

    @property
    def retriever(self):
        return self._retriever

    @retriever.setter
    def retriever(self, value: Chroma):
        self._retriever = value.as_retriever()

    async def summarize(self, window: str = "4min"):
        """Summarise the transciptions over passed window."""
        logger.info("Started summarising...")
        df = self.resample(window=window)
        docs = get_docs_from_df(df=df)
        summary = await summary_chain.arun(docs)
        self.summary = summary
        return summary

    async def load_in_chroma(self, window: str = "1min"):
        """Loads the data into ephemeral (in-memory) client"""
        logger.info("Preparing for QA documents")
        docs = get_docs_from_df(self.resample(window=window))
        collection = await Chroma.afrom_documents(
            documents=docs, embedding=settings.embed_model
        )
        self.retriever = collection
        return collection

    async def ingest_data(
        self, summary_window: str = "4min", qa_window: str = "1min", session_state=None
    ):
        session_state["summary"] = await self.summarize(window=summary_window)
        await self.load_in_chroma(window=qa_window)
        logger.info("Ingestion Completed!")
        docs = self.retriever.get_relevant_documents(
            "what is it that author is talking about?"
        )
        logger.info(f"answer from retriever: {docs}")
        return True
