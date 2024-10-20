from pydantic import BaseModel


class Add2(BaseModel):
    x: int
    y: int
