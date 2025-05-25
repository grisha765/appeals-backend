from enum import Enum
from pydantic import (
    BaseModel,
    Field,
    model_validator
)
from typing import (
        Optional,
        List
)


# ping schemas
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


# conversion schemas
class ConversionStatus(str, Enum):
    unviewed    = "unviewed"
    accepted    = "accepted"
    in_progress = "progress"
    executed    = "executed"
    closed      = "closed"


class ConversionCreateBody(BaseModel):
    user_id: int = Field(..., description="Owner of the conversion")
    head: str = Field(..., description="Short title")
    text: str = Field(..., description="Full text")
    status: ConversionStatus = Field(default=ConversionStatus.unviewed)


class ConversionStatusUpdateBody(BaseModel):
    status: ConversionStatus


class ConversionBrief(BaseModel):
    id: int
    head: str
    status: ConversionStatus


class ConversionDetail(BaseModel):
    id: int
    user_id: int
    head: str
    text: str
    status: ConversionStatus


class ConversionFileMeta(BaseModel):
    id: int
    filename: str
    content_type: str
    download_url: str


class ConversionText(BaseModel):
    text: str
    files: Optional[List[ConversionFileMeta]] = None


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
