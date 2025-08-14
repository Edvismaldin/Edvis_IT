from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.room import Room


def create_room(db: Session, *, name: str, capacity: int, location: str | None = None, resources: str | None = None) -> Room:
	room = Room(name=name, capacity=capacity, location=location, resources=resources)
	db.add(room)
	db.commit()
	db.refresh(room)
	return room


def get_room(db: Session, room_id: int) -> Room | None:
	return db.get(Room, room_id)


def get_room_by_name(db: Session, name: str) -> Room | None:
	stmt = select(Room).where(Room.name == name)
	return db.execute(stmt).scalars().first()


def list_rooms(db: Session, *, skip: int = 0, limit: int = 100) -> list[Room]:
	stmt = select(Room).offset(skip).limit(limit)
	return list(db.execute(stmt).scalars().all())