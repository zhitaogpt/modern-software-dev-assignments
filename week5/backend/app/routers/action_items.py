from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select, update
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import (
    ActionItemCreate,
    ActionItemRead,
    BulkCompleteRequest,
    Envelope,
    PaginatedResponse,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=Envelope[PaginatedResponse[ActionItemRead]])
def list_items(
    completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
) -> Envelope[PaginatedResponse[ActionItemRead]]:
    query = select(ActionItem).order_by(desc(ActionItem.created_at))
    if completed is not None:
        query = query.where(ActionItem.completed == completed)
    
    # Total count
    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    
    # Pagination
    offset = (page - 1) * page_size
    rows = db.execute(query.offset(offset).limit(page_size)).scalars().all()
    
    data = PaginatedResponse(
        items=[ActionItemRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )
    return Envelope(data=data)


@router.post("/", response_model=Envelope[ActionItemRead], status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> Envelope[ActionItemRead]:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return Envelope(data=ActionItemRead.model_validate(item))


@router.put("/{item_id}/complete", response_model=Envelope[ActionItemRead])
def complete_item(item_id: int, db: Session = Depends(get_db)) -> Envelope[ActionItemRead]:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    return Envelope(data=ActionItemRead.model_validate(item))


@router.post("/bulk-complete", response_model=Envelope[dict])
def bulk_complete(payload: BulkCompleteRequest, db: Session = Depends(get_db)) -> Envelope[dict]:
    db.execute(
        update(ActionItem)
        .where(ActionItem.id.in_(payload.item_ids))
        .values(completed=True)
    )
    # Note: get_db handles the final commit
    return Envelope(data={"count": len(payload.item_ids)})
