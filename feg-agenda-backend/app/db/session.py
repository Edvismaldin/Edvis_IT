from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


DATABASE_URL = f"sqlite:///{settings.sqlite_db_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)