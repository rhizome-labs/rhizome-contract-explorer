from pathlib import Path

import yaml

from rhizome_contract_explorer.app.models import AppConfig


class Config:

    CONFIG_FILE_PATH = f"{Path(__file__).parent.parent}/config.yml"

    def __init__(self) -> None:
        pass

    @classmethod
    def load_config(cls) -> AppConfig:
        with open(cls.CONFIG_FILE_PATH, "r") as f:
            config = yaml.safe_load(f)
        config = AppConfig(**config)
        return config
