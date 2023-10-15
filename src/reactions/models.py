from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class Reaction(Base):
    __tablename__ = "reaction"
    reaction_id: int = Column(Integer, primary_key=True, autoincrement=True)
    reaction: str = Column(String, nullable=False)
    post_uuid: str = Column(String, nullable=False)
