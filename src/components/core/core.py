import threading
from loguru import logger

from components.utils.config import BotConfig


class Bot(threading.Thread):
    def __init__(self, config: BotConfig) -> None:
        threading.Thread.__init__(self)
        logger.info(
            f"Account loaded: {config.clientName}, version: {config.clientVersion}"
        )

    def run(self):
        print("ok")
