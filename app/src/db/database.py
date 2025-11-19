from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.src.config.config import settings

Base = declarative_base()

engine = create_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
