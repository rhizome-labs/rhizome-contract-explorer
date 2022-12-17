from pydantic import BaseModel


class AppConfig(BaseModel):
    api_endpoint: str
    block_refresh: int
    network_id: int
