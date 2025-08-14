from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.event import EventCreate, EventRead
from app.crud.event import create_event, list_events
from app.deps import get_db, get_current_active_user

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead)
def create_event_endpoint(payload: EventCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
	try:
		return create_event(
			db,
			title=payload.title,
			description=payload.description,
			room_id=payload.room_id,
			owner_id=current_user.id,
			start_time=payload.start_time,
			end_time=payload.end_time,
			status=payload.status,
		)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[EventRead])
def list_events_endpoint(
	room_id: int | None = None,
	owner_id: int | None = None,
	start: datetime | None = Query(None),
	end: datetime | None = Query(None),
	db: Session = Depends(get_db),
	_: str = Depends(get_current_active_user),
):
	return list_events(db, room_id=room_id, owner_id=owner_id, start=start, end=end)