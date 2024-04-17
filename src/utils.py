import re


def clean_text(text: str):
    """Cleans most common filter words that occurs in a natural language"""
    filler_words = "uh, blah, um, umm, uhmmm, uhm, ah, so, like, well, then, yeah, okay, hey, huh, yes, no, hmm, huh?, er, sure, cool".split(
        ","
    )
    filler_regex = re.compile("|".join(map(re.escape, filler_words)))
    return filler_regex.sub("", text)


# from .ai.tasks import LLMTasks
# class Process:
#     def __init__(self, video_url: str) -> None:
#         self.yt = Youtube.from_video_url(video_url=video_url)
#         self.tasks = LLMTasks.run_through_pandas(self.yt.transcript_data, column="text")
