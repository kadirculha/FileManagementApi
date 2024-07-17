from typing import Dict, Any
from pydantic import BaseModel, ValidationError, validator

class Corridor(BaseModel):
    id: str
    content: Dict[str, Any]  # İçeriğin yapısı net olmadığı için genel bir sözlük türünde tanımlandı

    @validator("content")
    def validate_content_data(cls, v):
        if not v:
            raise ValueError("content field cannot be empty")
        return v

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
