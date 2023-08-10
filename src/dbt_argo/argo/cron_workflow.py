from typing import Literal

from pydantic import BaseModel

from .cron_workflow_spec import CronWorkflowSpec
from .metadata import Metadata
from .workflow_spec import WorkflowSpec


class CronWorkflow(BaseModel):
    """CronWorkflow model"""

    kind: Literal["CronWorkflow"]
    metadata: Metadata
    spec: CronWorkflowSpec

    def set_workflow_spec(self, workflow_spec: WorkflowSpec):
        self.spec.workflowSpec = workflow_spec
        return self
