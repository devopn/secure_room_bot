import dataclasses
import os
@dataclasses.dataclass
class Config:
    host: str


config = Config(host=os.environ.get("HOST", "127.0.0.1:8000"))