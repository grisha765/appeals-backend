from typing import Optional, Literal
from pydantic import BaseModel, Field, model_validator


class PingResponse(BaseModel):
    Pong: str


class PingBody(BaseModel):
    op: Literal[
    "plus",
    "minus",
    "reset",
    "int"
] = Field(
        default="plus",
        description="Counter operation"
    )
    value: Optional[int] = Field(
        default=None,
        description="Number for op=‘int’; ignored otherwise",
    )

    @model_validator(mode="after")
    def validate_int(self) -> "PingBody":
        if self.op == "int":
            if self.value is None:
                raise ValueError("The ‘value’ field is required for op='int'")
        elif self.value is not None:
            raise ValueError("The ‘value’ field is only used when op='int'")
        return self


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
