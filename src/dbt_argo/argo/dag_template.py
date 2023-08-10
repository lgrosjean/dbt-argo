"""
Source: https://argoproj.github.io/argo-workflows/fields/#dagtask
"""

from typing import List

from pydantic import BaseModel

from .dag_task import DAGTask


class DAGTemplate(BaseModel):
    """DAGTemplate is a template subtype for directed acyclic graph templates"""

    tasks: List[DAGTask]
