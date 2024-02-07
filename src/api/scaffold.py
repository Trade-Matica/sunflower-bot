from loguru import logger
import os

from components.utils.config import Config
from components.core.core import Bot


def initialise():
    os.system("cls||clear")


class Scaffold:
    @staticmethod
    @logger.catch
    def init():
        """
        Usage: python main.py init

        Create defaut files and initialise config
        """

        initialise()
        Config.gather()

    @staticmethod
    @logger.catch
    def run():
        """
        Usage: python main.py run

        Start the bot
        """

        initialise()

        accounts = Config.gather()
        logger.info(f"Starting bot on {len(accounts)} account(s).")

        for account in accounts:
            Bot(account).start()
