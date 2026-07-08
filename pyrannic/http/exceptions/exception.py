from pydantic import BaseModel


class HttpExceptionResponse(BaseModel):
    loc: list[str]
    msg: str
    type: str
