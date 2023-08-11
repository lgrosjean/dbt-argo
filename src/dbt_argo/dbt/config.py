from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    enabled: bool
    alias: Optional[str] = None
    schema_: Optional[str] = Field(alias="schema")
    database: Optional[str] = None
    tags: List[str]
    materialized: Literal["table", "view", "test", "seed", "ephemeral"]
