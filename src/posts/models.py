from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import Column, Integer, String, ARRAY, Text, ForeignKey

from src.users.models import User


Base: DeclarativeMeta = declarative_base()


class Post(Base):
    __tablename__ = "post"
    post_id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    post_text: str = Column(Text, nullable=False)
    user_uuid: str = Column(String, ForeignKey(User.user_uuid), nullable=False)
    post_uuid: str = Column(String, unique=True, nullable=False)
    reactions: list = Column(ARRAY(String))
