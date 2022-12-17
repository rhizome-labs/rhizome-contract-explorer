import os
from datetime import datetime
from functools import lru_cache

from dotenv import dotenv_values
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


# Load environment variables.
@lru_cache(maxsize=1)
def env():
    return dict(dotenv_values())


# Load Jinja2 templates
@lru_cache(maxsize=1)
def load_templates():
    return Jinja2Templates(directory=f"{os.path.dirname(__file__)}/app/templates")


ENV = env()
TEMPLATES = load_templates()
CURRENT_YEAR = datetime.now().year
