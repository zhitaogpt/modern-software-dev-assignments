from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from .. import db, schemas


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=schemas.NoteRead)
def create_note(note_in: schemas.NoteCreate) -> schemas.NoteRead:
    content = note_in.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content cannot be empty")
    
    note_id = db.insert_note(content)
    row = db.get_note(note_id)
    if not row:
        raise HTTPException(status_code=500, detail="Failed to retrieve created note")
    
    return schemas.NoteRead(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"]
    )


@router.get("", response_model=List[schemas.NoteRead])
def list_notes() -> List[schemas.NoteRead]:
    rows = db.list_notes()
    return [
        schemas.NoteRead(
            id=r["id"],
            content=r["content"],
            created_at=r["created_at"]
        )
        for r in rows
    ]


@router.get("/{note_id}", response_model=schemas.NoteRead)
def get_single_note(note_id: int) -> schemas.NoteRead:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    
    return schemas.NoteRead(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"]
    )


