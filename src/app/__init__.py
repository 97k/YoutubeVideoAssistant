from app.config import Settings, Models

settings = Settings()
from helpers import set_configs

set_configs(Models.MIXTRAL_8_7B_INSTRUCT)

from app.data import Youtube
