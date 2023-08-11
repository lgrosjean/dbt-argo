"""
Source: https://argoproj.github.io/argo-workflows/fields/#parameter
"""

from typing import Optional

from pydantic import BaseModel


class Parameter(BaseModel):
    name: str
    # https://docs.pydantic.dev/latest/migration/#required-optional-and-nullable-fields
    value: Optional[str] = None
