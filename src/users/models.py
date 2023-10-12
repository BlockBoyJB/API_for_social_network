from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, unique=True, nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("total_reactions", Integer, default=0, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("user_uuid", String, unique=True, nullable=False)
)
