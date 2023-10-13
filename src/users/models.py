from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    total_reactions: int = Column(Integer, default=0, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    user_uuid: str = Column(String, unique=True, nullable=False)


class UserVerifyingCode(Base):
    __tablename__ = "user_verifying_code"
    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=False)
    verifying_uuid: str = Column(String, nullable=False)
