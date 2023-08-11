from typing import Union

from pydantic import Field, TypeAdapter
from typing_extensions import Annotated

from .cron_workflow import CronWorkflow
from .workflow import Workflow

# https://docs.pydantic.dev/latest/usage/types/unions/#nested-discriminated-unions
BaseWorkflow = Annotated[
    Union[
        CronWorkflow,
        Workflow,
    ],
    Field(discriminator="kind"),
]


# See: https://github.com/pydantic/pydantic/discussions/4950#discussioncomment-5775767
def WorkflowFactory(data):
    return TypeAdapter(BaseWorkflow).validate_python(data)
