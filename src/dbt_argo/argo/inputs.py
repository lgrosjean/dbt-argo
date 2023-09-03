"""
Source: https://argoproj.github.io/argo-workflows/fields/#inputs
"""
from typing import List, Optional

from pydantic import BaseModel

from .artifact import Artifact
from .parameter import Parameter


class Inputs(BaseModel):
    """Inputs Base model"""

    artifacts: Optional[List[Artifact]] = None
    parameters: Optional[List[Parameter]] = None
