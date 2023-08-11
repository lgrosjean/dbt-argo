from typing import Optional

from pydantic import BaseModel

from .workflow_spec import WorkflowSpec


class CronWorkflowSpec(BaseModel):
    """CronWorkflowSpec reference"""

    suspend: bool = False
    schedule: str
    timezone: str = "Europe/Paris"
    concurrencyPolicy: str = "Replace"
    workflowSpec: Optional[WorkflowSpec] = WorkflowSpec()
