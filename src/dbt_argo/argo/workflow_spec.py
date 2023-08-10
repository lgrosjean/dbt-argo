"""Source: https://argoproj.github.io/argo-workflows/fields/#workflowspec"""
import os
from typing import List, Optional

from pydantic import BaseModel

from .template import Template

_K8S_SA = os.getenv("K8S_SA", "pipeline")


class WorkflowSpec(BaseModel):
    """WorkflowSpec reference"""

    entrypoint: str = "pipeline"
    serviceAccountName: str = _K8S_SA
    templates: Optional[List[Template]] = None
