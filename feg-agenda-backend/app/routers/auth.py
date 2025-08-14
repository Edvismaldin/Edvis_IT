from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user import authenticate
from app.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login_for_access_token(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db),
):
	user = authenticate(db, email=form_data.username, password=form_data.password)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
	access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
	token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
	return {"access_token": token, "token_type": "bearer"}