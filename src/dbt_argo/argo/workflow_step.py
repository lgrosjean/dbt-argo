"""
Source: https://argoproj.github.io/argo-workflows/fields/#workflowstep
"""

from typing import Optional

from pydantic import BaseModel

from .arguments import Arguments


class WorkflowStep(BaseModel):
    """WorkflowStep is a reference to a template to execute in a series of step"""

    name: str
    template: str
    arguments: Optional[Arguments] = None
