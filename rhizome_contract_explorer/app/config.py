from pathlib import Path

import yaml

from rhizome_contract_explorer.app.models import AppConfig


class Config:

    CONFIG_FILE_PATH = f"{Path(__file__).parent.parent}/config.yml"

    DEFAULT_CONFIG = {
        "api_endpoint": "https://api.icon.community",
        "network_id": 1,
        "block_refresh": 2,
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def load_config(cls) -> AppConfig:
        try:
            with open(cls.CONFIG_FILE_PATH, "r") as f:
                config = yaml.safe_load(f)
                config = AppConfig(**config)
        except FileNotFoundError:
            config = AppConfig(**cls.DEFAULT_CONFIG)
        return config
