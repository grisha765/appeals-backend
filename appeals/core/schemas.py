from enum import Enum
from pydantic import BaseModel, Field, model_validator


class PingResponse(BaseModel):
    Pong: str


class Op(str, Enum):
    plus  = "plus"
    minus = "minus"
    reset = "reset"
    set  = "set"


class PingBody(BaseModel):
    op: Op = Field(
        default=Op.plus,
        description="Counter operation"
    )
    value: int | None = Field(
        default=None,
        description="Used only for op='int'"
    )

    @model_validator(mode="after")
    def validate_int(self):
        if self.op is Op.set and self.value is None:
            raise ValueError("The ‘value’ field is required for op='set'")
        return self


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
