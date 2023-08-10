"""
Source: https://argoproj.github.io/argo-workflows/fields/#container
"""
from typing import List, Optional

from pydantic import BaseModel

from .envvar import EnvVar
from .resources import Resources


class Container(BaseModel):
    """Container base model"""

    image: str
    command: List[str]
    workingDir: str = "/app"
    args: List[str] = []
    env: Optional[EnvVar] = None
    resources: Optional[Resources] = Resources()
