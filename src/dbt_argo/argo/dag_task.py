"""
Source: https://argoproj.github.io/argo-workflows/fields/#dagtask
"""

from typing import List, Optional

from pydantic import BaseModel

from .arguments import Arguments


class DAGTask(BaseModel):
    """DAGTask represents a node in the graph during DAG execution"""

    name: str
    template: str
    arguments: Optional[Arguments] = None
    dependencies: List[str] = []
