from loguru import logger
from pathlib import Path
from typing import List
import json


class BotConfig:
    def __init__(
        self,
        authorization: str,
        clientVersion: str,
        clientName: str,
    ) -> None:
        self.authorization = authorization
        self.clientVersion = clientVersion
        self.clientName = clientName


class Config:
    @staticmethod
    @logger.catch
    def __config_to_list(config: dict) -> List[BotConfig]:
        configs = []

        for account in config:
            configs.append(
                BotConfig(
                    authorization=account["authorization"],
                    clientVersion=account["clientVersion"],
                    clientName=account["clientName"],
                ),
            )

        return configs

    @staticmethod
    @logger.catch
    def gather() -> List[BotConfig]:
        """
        Check if a config JSON file exists at the specified path. If not, create one with default data.
        """

        file_path = Path("../script/config.json").resolve()

        if file_path.exists():
            logger.info("Config file found. Loading existing configuration.")
            with open(file_path, "r") as file:
                return Config.__config_to_list(
                    json.load(file),
                )

        logger.info("No configuration file found, starting setup.")
        logger.info(f"Default config file created at {file_path.absolute()}")

        return Config.__config_to_list(
            Config.setup_config(file_path),
        )

    @staticmethod
    def setup_config(file_path: Path) -> dict:
        """
        Set up the configuration.
        """

        data = [
            {
                "authorization": "Bearer eyJhbG....",
                "clientVersion": "2024-02-07T02:00",
                "clientName": "your account name",
            }
        ]

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        return data
