from typing import Optional

from pydantic import BaseModel, model_validator


class EnvVar(BaseModel):
    name: str
    value: str = ""
    value_from: Optional[str]

    # https://docs.pydantic.dev/latest/usage/validators/#model-validators
    @model_validator(mode="after")
    def check_value_from(self) -> "EnvVar":
        if self.value != "" and self.value_from is not None:
            raise ValueError("`value_from` cannot be used if `value` is not empty.")
        return self
