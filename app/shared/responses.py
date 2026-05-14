from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

    @classmethod
    def success_response(cls, message: str, data: Any = None):
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_response(cls, message: str, data: Any = None):
        return cls(success=False, message=message, data=data)