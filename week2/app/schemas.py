from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class ActionItemBase(BaseModel):
    text: str
    done: bool = False


class ActionItemCreate(ActionItemBase):
    note_id: Optional[int] = None


class ActionItemRead(ActionItemBase):
    id: int
    note_id: Optional[int] = None
    created_at: str


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: str


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemRead]


class MarkDoneRequest(BaseModel):
    done: bool = True
