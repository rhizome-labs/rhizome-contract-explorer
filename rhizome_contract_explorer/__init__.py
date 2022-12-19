import logging
import logging.config
import os
from datetime import datetime
from logging.config import dictConfig

from dotenv import dotenv_values
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from rhizome_contract_explorer.app.config import Config


# Load private key.
def load_private_key() -> str | None:
    env = dict(dotenv_values())
    try:
        private_key = env["PRIVATE_KEY"]
        return private_key
    except KeyError:
        return None


# Load Jinja2 templates
def load_templates():
    return Jinja2Templates(directory=f"{os.path.dirname(__file__)}/app/templates")


CONFIG = Config.load_config()
TEMPLATES = load_templates()
CURRENT_YEAR = datetime.now().year


PK = load_private_key()
if PK is None:
    MODE = "R"
else:
    MODE = "RW"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(levelprefix)s %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("app")
