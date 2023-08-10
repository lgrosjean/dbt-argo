"""
Source: https://argoproj.github.io/argo-workflows/fields/#resourcerequirements
"""

from pydantic import BaseModel

from .quantity import Limits, Requests


class Resources(BaseModel):
    """ResourceRequirements describes the compute resource requirements."""

    limits: Limits = Limits()
    requests: Requests = Requests()
