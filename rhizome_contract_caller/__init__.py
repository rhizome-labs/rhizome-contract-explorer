import os
from datetime import datetime
from functools import lru_cache

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


@lru_cache(maxsize=1)
def env():
    load_dotenv()
    return {
        "API_ENDPOINT": os.getenv("API_ENDPOINT"),
        "NID": os.getenv("NID"),
        "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
    }


# Load Jinja2 templates
@lru_cache(maxsize=1)
def load_templates():
    return Jinja2Templates(directory=f"{os.path.dirname(__file__)}/app/templates")


ENV = env()
TEMPLATES = load_templates()

CURRENT_YEAR = datetime.now().year
