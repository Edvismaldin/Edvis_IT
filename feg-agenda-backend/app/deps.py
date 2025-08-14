from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		user_id: str | None = payload.get("sub")
		if user_id is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	user = db.get(User, int(user_id))
	if user is None:
		raise credentials_exception
	return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
	if not current_user.is_active:
		raise HTTPException(status_code=400, detail="Inactive user")
	return current_user


def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
	if not current_user.is_superuser:
		raise HTTPException(status_code=403, detail="Not enough permissions")
	return current_user