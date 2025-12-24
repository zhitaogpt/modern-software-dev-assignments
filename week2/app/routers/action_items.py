from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from .. import db, schemas
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=schemas.ExtractResponse)
def extract(request: schemas.ExtractRequest) -> schemas.ExtractResponse:
    return _extract_internal(request, use_llm=False)


@router.post("/extract-llm", response_model=schemas.ExtractResponse)
def extract_llm(request: schemas.ExtractRequest) -> schemas.ExtractResponse:
    return _extract_internal(request, use_llm=True)


def _extract_internal(request: schemas.ExtractRequest, use_llm: bool) -> schemas.ExtractResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if request.save_note:
        note_id = db.insert_note(text)

    if use_llm:
        items = extract_action_items_llm(text)
    else:
        items = extract_action_items(text)
        
    ids = db.insert_action_items(items, note_id=note_id)
    
    # Fetch full objects to return consistent data
    rows = db.list_action_items(note_id=note_id)
    
    extracted_items = []
    # If it was saved as a note, we can filter by that note_id
    if note_id:
        extracted_items = [
            schemas.ActionItemRead(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"]
            )
            for r in rows if r["id"] in ids
        ]
    else:
        # Fallback for unsaved notes, but since they are in DB now, 
        # we can just return what we have from ids.
        for i, t in zip(ids, items):
            extracted_items.append(schemas.ActionItemRead(
                id=i, text=t, done=False, created_at="just now"
            ))

    return schemas.ExtractResponse(note_id=note_id, items=extracted_items)


@router.get("", response_model=List[schemas.ActionItemRead])
def list_all(note_id: Optional[int] = None) -> List[schemas.ActionItemRead]:
    rows = db.list_action_items(note_id=note_id)
    return [
        schemas.ActionItemRead(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=schemas.ActionItemBase)
def mark_done(action_item_id: int, request: schemas.MarkDoneRequest) -> schemas.ActionItemBase:
    db.mark_action_item_done(action_item_id, request.done)
    return schemas.ActionItemBase(text="Updated", done=request.done)


