from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .columns import Column
from .config import Config


class Node(BaseModel):
    database: str
    schema_: str = Field(alias="schema")
    node_name: str = Field(alias="name")
    resource_type: Literal["model", "test", "macro", "seed"]
    unique_id: str
    alias: str
    config: Config
    description: Optional[str] = None
    columns: Dict[str, Column]
    compiled_code: Optional[str] = None
    depends_on: Dict[str, List[str]]

    @property
    def name(self):
        return str(self.node_name).replace("_", "-").strip("-")

    @property
    def is_model(self):
        return self.resource_type == "model"

    @property
    def is_view(self):
        return self.config.materialized == "view"

    @property
    def is_ephemeral(self):
        return self.config.materialized == "ephemeral"

    @property
    def is_table(self):
        return self.config.materialized == "table"

    @property
    def dependencies(self):
        return self.depends_on.get("nodes", [])
