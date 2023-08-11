from pydantic import BaseModel


class Column(BaseModel):
    name: str
    description: str = ""
