from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
import app.models  # noqa: F401
from app.crud.user import create_user, get_user_by_email
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

from app.routers import auth as auth_router
from app.routers import users as users_router
from app.routers import rooms as rooms_router
from app.routers import events as events_router


app = FastAPI(title=settings.project_name)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
	# Create tables
	Base.metadata.create_all(bind=engine)
	# Seed admin
	db: Session = SessionLocal()
	try:
		if not get_user_by_email(db, settings.admin_email):
			create_user(db, email=settings.admin_email, full_name="Administrador", password=settings.admin_password, is_superuser=True)
	finally:
		db.close()


@app.get("/")
def read_root():
	return {"name": settings.project_name}


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(rooms_router.router)
app.include_router(events_router.router)