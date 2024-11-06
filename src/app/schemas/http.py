from pydantic import BaseModel

__all__ = ["HTTP404"]


# https://stackoverflow.com/questions/64501193/fastapi-how-to-use-httpexception-in-responses
class HTTP404(BaseModel):
    detail: str

    # class Config:
    #   schema_extra = {"example": {"details": "HTTPException raised."}}
    model_config = {
        "json_schema_extra": {"example": {"details": "HTTPException raised."}}
    }
