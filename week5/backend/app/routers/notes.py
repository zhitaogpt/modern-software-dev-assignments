from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, Tag
from ..schemas import Envelope, NoteCreate, NoteRead, NoteUpdate, PaginatedResponse
from ..services.extract import extract_tags

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=Envelope[PaginatedResponse[NoteRead]])
def list_notes(
    q: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    sort: str = "created_desc",
    db: Session = Depends(get_db),
) -> Envelope[PaginatedResponse[NoteRead]]:
    query = select(Note)
    if q:
        query = query.where((Note.title.ilike(f"%{q}%")) | (Note.content.ilike(f"%{q}%")))

    # Total count
    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0

    # Sorting
    if sort == "title_asc":
        query = query.order_by(Note.title.asc())
    elif sort == "created_desc":
        query = query.order_by(Note.created_at.desc())
    else:
        query = query.order_by(Note.created_at.desc())

    # Pagination
    offset = (page - 1) * page_size
    rows = db.execute(query.offset(offset).limit(page_size)).scalars().all()

    data = PaginatedResponse(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )
    return Envelope(data=data)


@router.post("/", response_model=Envelope[NoteRead], status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> Envelope[NoteRead]:
    note = Note(title=payload.title, content=payload.content)
    
    # Extract and attach tags
    tag_names = extract_tags(payload.content)
    if tag_names:
        for name in set(tag_names): # Unique tags per note
            tag = db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none()
            if not tag:
                tag = Tag(name=name)
                db.add(tag)
            note.tags.append(tag)
            
    db.add(note)
    db.flush()
    db.refresh(note)
    return Envelope(data=NoteRead.model_validate(note))


@router.get("/{note_id}", response_model=Envelope[NoteRead])
def get_note(note_id: int, db: Session = Depends(get_db)) -> Envelope[NoteRead]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return Envelope(data=NoteRead.model_validate(note))


@router.put("/{note_id}", response_model=Envelope[NoteRead])
def update_note(
    note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)
) -> Envelope[NoteRead]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
        # Re-extract tags if content changed
        tag_names = extract_tags(payload.content)
        # Clear existing tags and re-add (simple strategy)
        note.tags = []
        if tag_names:
            for name in set(tag_names):
                tag = db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none()
                if not tag:
                    tag = Tag(name=name)
                    db.add(tag)
                note.tags.append(tag)

    db.add(note)
    db.flush()
    db.refresh(note)
    return Envelope(data=NoteRead.model_validate(note))


@router.delete("/{note_id}", response_model=Envelope[dict])
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Envelope[dict]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    return Envelope(data={"deleted_id": note_id})
