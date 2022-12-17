import os
from datetime import datetime

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
