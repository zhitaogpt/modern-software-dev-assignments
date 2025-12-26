from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetails(BaseModel):
    code: str
    message: str


class Envelope(BaseModel, Generic[T]):
    ok: bool = True
    data: Optional[T] = None
    error: Optional[ErrorDetails] = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class TagRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    tags: list[TagRead] = []

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BulkCompleteRequest(BaseModel):
    item_ids: list[int]
