"""
Source: https://argoproj.github.io/argo-workflows/fields/#inputs
"""
from typing import List

from pydantic import BaseModel

from .parameter import Parameter


class Inputs(BaseModel):
    """Inputs Base model"""

    parameters: List[Parameter]
