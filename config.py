import dataclasses
import os
@dataclasses.dataclass
class Config:
    host: str
    key: str


config = Config(
    host=os.environ.get("HOST", "127.0.0.1:8000"),
    key=os.environ.get("TG_KEY"),
    )