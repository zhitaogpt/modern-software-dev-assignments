from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str
    is_starred: bool = False
    # Optional: allow creating note with tags immediately
    tags: list[str] = Field(default_factory=list)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    is_starred: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagRead] = []


class NoteStats(BaseModel):
    total_count: int
    starred_count: int


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    is_starred: bool | None = None


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None


