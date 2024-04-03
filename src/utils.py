import requests
from .config import settings
from . import exceptions
from .logger import get_logger

logger = get_logger(__name__)


def callmodel(model_id, payload):
    """
    Calls the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/en/quicktour)
    """
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    try:
        response = requests.post(
            url := f"{settings.HF_INF_API}/{model_id}", headers=headers, json=payload
        )
        return response.json()
    except exceptions as e:
        logger.exception(
            err_msg := f"[Exception] occured while inferencing hugging face: {url=}|{response.text=:<15}|{response.status_code:<5}"
        )
        raise exceptions.HuggingFaceInferenceException(message=err_msg)


import re


def clean_text(text: str):
    """Cleans most common filter words that occurs in a natural language"""
    filler_words = "uh, blah, um, umm, uhmmm, uhm, ah, so, like, well, then, yeah, okay, hey, huh, yes, no, hmm, huh?, er, sure, cool".split(
        ","
    )
    filler_regex = re.compile("|".join(map(re.escape, filler_words)))
    return filler_regex.sub("", text)


from urllib.parse import urlparse, parse_qs


from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime as dt


class Youtube:
    def __init__(self, transcript_data: pd.DataFrame | None = None) -> None:
        self.transcript_data = transcript_data

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
    def from_video_url(cls, video_url: str, window: str = "30s", process: bool = True):
        # TODO: validate URL
        ts = cls.get_transcript(cls.get_yt_id(video_url))
        df = pd.DataFrame(ts)
        start = dt.datetime(year=2000, month=1, day=1)
        df.index = df["start"].apply(lambda x: dt.timedelta(seconds=x) + start)
        df["text"] = df["text"].apply(clean_text)
        df["text"] = df["text"] + " "
        df_text = (
            df[["text", "start"]].resample("1min").agg({"text": sum, "start": list})
        )
        return cls(df_text)
