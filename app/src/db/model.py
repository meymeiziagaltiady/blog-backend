from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.src.db.database import Base


class UserRole(str, PyEnum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)

    contents = relationship("Content", back_populates="owner", cascade="all, delete")


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="contents")
