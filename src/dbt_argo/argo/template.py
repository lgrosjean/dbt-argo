"""
Source: https://argoproj.github.io/argo-workflows/fields/#template
"""
from typing import List, Optional

from pydantic import BaseModel, model_validator

from .container import Container
from .dag_template import DAGTemplate
from .inputs import Inputs
from .workflow_step import WorkflowStep


class Template(BaseModel):
    """Template is a reusable and composable unit of execution in a workflow"""

    name: str
    container: Optional[Container] = None
    inputs: Optional[Inputs] = None
    dag: Optional[DAGTemplate] = None
    steps: Optional[List[List[WorkflowStep]]] = None

    # https://docs.pydantic.dev/latest/usage/validators/#model-validators
    @model_validator(mode="after")
    def check_template(self) -> "Template":
        if (self.container is None) ^ (self.dag is None) ^ (self.steps is None):
            raise ValueError(
                "`Only one from container, dag or template should be given."
            )
        return self
