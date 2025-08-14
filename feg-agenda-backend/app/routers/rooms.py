from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.room import RoomCreate, RoomRead
from app.crud.room import create_room, get_room, get_room_by_name, list_rooms
from app.deps import get_db, get_current_active_user, get_current_superuser

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/", response_model=RoomRead, dependencies=[Depends(get_current_superuser)])
def create_room_endpoint(payload: RoomCreate, db: Session = Depends(get_db)):
	existing = get_room_by_name(db, payload.name)
	if existing:
		raise HTTPException(status_code=400, detail="Nome de sala já existe")
	return create_room(db, name=payload.name, capacity=payload.capacity, location=payload.location, resources=payload.resources)


@router.get("/{room_id}", response_model=RoomRead)
def get_room_endpoint(room_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_active_user)):
	room = get_room(db, room_id)
	if not room:
		raise HTTPException(status_code=404, detail="Sala não encontrada")
	return room


@router.get("/", response_model=list[RoomRead])
def list_rooms_endpoint(db: Session = Depends(get_db), _: str = Depends(get_current_active_user)):
	return list_rooms(db)