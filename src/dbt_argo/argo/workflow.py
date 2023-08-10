from typing import Literal

from pydantic import BaseModel

from .metadata import Metadata
from .workflow_spec import WorkflowSpec


class Workflow(BaseModel):
    """Workflow model"""

    kind: Literal["Workflow"]
    metadata: Metadata
    spec: WorkflowSpec

    def set_workflow_spec(self, workflow_spec: WorkflowSpec):
        self.spec = workflow_spec
        return self
