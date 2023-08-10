"""
Source: https://argoproj.github.io/argo-workflows/fields/#arguments
"""

from typing import List

from pydantic import BaseModel

from .parameter import Parameter


class Arguments(BaseModel):
    """Arguments to a template"""

    parameters: List[Parameter] = []
