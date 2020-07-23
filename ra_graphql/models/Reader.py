import sqlalchemy
from application import metadata
from permissions_system.constants import InternalTables

_reader_table_name = "readers"

Reader = sqlalchemy.Table(
    _reader_table_name,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.ForeignKey(
        f"{InternalTables.User}.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(
        length=500), unique=True, nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(
        length=100
    ), unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=300)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(
        timezone=True), nullable=False),
    sqlalchemy.Column("updated_at",
                      sqlalchemy.DateTime(timezone=True), nullable=False)
)
