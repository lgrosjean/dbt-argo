import json
from os import getcwd, getenv, path
from typing import Dict, Optional

from pydantic import BaseModel, field_validator

from .node import Node


class Manifest(BaseModel):
    nodes: Dict[str, Node]

    @field_validator("nodes")
    @classmethod
    def nodes_are_models(cls, nodes: Dict[str, Node]) -> Dict[str, Node]:
        return {node_name: node for node_name, node in nodes.items() if node.is_model}

    @classmethod
    def load(cls, manifest_path: Optional[str] = None):
        """Load a Manifest class from manifest file path."""

        if not manifest_path:
            manifest_path = path.join(
                getenv("DBT_TARGET_DIR", getcwd()), "manifest.json"
            )

        with open(manifest_path, "r", encoding="utf8") as manifest_file:
            manifest_dict = json.load(manifest_file)
        return cls(**manifest_dict)

    def get_dependencies(self, node: Node):
        return [
            self.nodes[dependency].name
            for dependency in node.dependencies
            if dependency in self.nodes and self.nodes[dependency].is_model
        ]
