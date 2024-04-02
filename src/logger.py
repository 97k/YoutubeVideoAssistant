import logging

logging.basicConfig(
    filename="./yt_qa_sum.log",
    format="%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)


def get_logger(name: str|None = None):
    return logging.getLogger(name=name)