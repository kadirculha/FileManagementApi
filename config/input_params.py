from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError, validator

class Corridor(BaseModel):
    id: str
    content: Optional[Any] = None  # İçeriğin boş olmasına izin veriyoruz

    @validator('content', pre=True, always=True)
    def set_default_content(cls, v):
        return v if v is not None else {}

class RequestItem(BaseModel):
    eventType: str
    companyId: int
    corridor: Corridor

    @validator("eventType")
    def validate_event_type(cls, v):
        allowed_event_types = {"INSERT", "UPDATE", "DELETE"}
        if v not in allowed_event_types:
            raise ValueError(f"eventType must be one of {allowed_event_types}")
        return v
