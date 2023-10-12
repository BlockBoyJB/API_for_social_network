from src.users.models import user
from sqlalchemy import MetaData, Table, Column, Integer, String, ARRAY, Text, ForeignKey

metadata = MetaData()

post = Table(
    "post",
    metadata,
    Column("post_id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("username", String, nullable=False),
    Column("post_text", Text, nullable=False),
    Column("user_uuid", String, ForeignKey(user.c.user_uuid), nullable=False),
    Column("post_uuid", String, unique=True, nullable=False),
    Column("reactions", ARRAY(String))
)
