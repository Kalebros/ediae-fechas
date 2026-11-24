from pydantic import BaseModel
from typing import List
from pydantic import Field, ConfigDict
from datetime import date

class Usuario(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    vacaciones: List[date] = Field(default_factory=list)

