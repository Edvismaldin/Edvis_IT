from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from datetime import datetime
from app.models.event import Event


def has_conflict(db: Session, *, room_id: int, start_time: datetime, end_time: datetime, exclude_event_id: int | None = None) -> bool:
	conditions = [
		Event.room_id == room_id,
		or_(
			and_(Event.start_time <= start_time, Event.end_time > start_time),
			and_(Event.start_time < end_time, Event.end_time >= end_time),
			and_(Event.start_time >= start_time, Event.end_time <= end_time),
		),
	]
	if exclude_event_id is not None:
		conditions.append(Event.id != exclude_event_id)
	stmt = select(Event).where(and_(*conditions))
	return db.execute(stmt).scalars().first() is not None


def create_event(db: Session, *, title: str, description: str | None, room_id: int, owner_id: int, start_time: datetime, end_time: datetime, status: str = "confirmed") -> Event:
	if has_conflict(db, room_id=room_id, start_time=start_time, end_time=end_time):
		raise ValueError("Conflito de horário para esta sala")
	event = Event(title=title, description=description, room_id=room_id, owner_id=owner_id, start_time=start_time, end_time=end_time, status=status)
	db.add(event)
	db.commit()
	db.refresh(event)
	return event


def list_events(db: Session, *, room_id: int | None = None, owner_id: int | None = None, start: datetime | None = None, end: datetime | None = None) -> list[Event]:
	stmt = select(Event)
	conditions = []
	if room_id is not None:
		conditions.append(Event.room_id == room_id)
	if owner_id is not None:
		conditions.append(Event.owner_id == owner_id)
	if start is not None:
		conditions.append(Event.end_time > start)
	if end is not None:
		conditions.append(Event.start_time < end)
	if conditions:
		stmt = stmt.where(and_(*conditions))
	stmt = stmt.order_by(Event.start_time.asc())
	return list(db.execute(stmt).scalars().all())