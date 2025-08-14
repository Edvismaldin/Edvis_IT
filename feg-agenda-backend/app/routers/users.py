from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user_by_email
from app.deps import get_db, get_current_superuser, get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, dependencies=[Depends(get_current_superuser)])
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
	existing = get_user_by_email(db, payload.email)
	if existing:
		raise HTTPException(status_code=400, detail="Email já cadastrado")
	user = create_user(db, email=payload.email, full_name=payload.full_name, password=payload.password)
	return user


@router.get("/me", response_model=UserRead)
def read_current_user(current_user=Depends(get_current_active_user)):
	return current_user