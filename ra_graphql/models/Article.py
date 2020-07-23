import sqlalchemy
from application import metadata
from permissions_system.constants import InternalTables
from models.Author import _author_table_name
from sqlalchemy.dialects.postgresql import (
    UUID
)

_article_table_name = "articles"

Article = sqlalchemy.Table(
    _article_table_name,
    metadata,
    sqlalchemy.Column("id", UUID, primary_key=True),
    sqlalchemy.Column("author_id", sqlalchemy.ForeignKey(
        f"{_author_table_name}.id", ondelete="CASCADE")
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(
        timezone=True), nullable=False),
    sqlalchemy.Column("updated_at",
                      sqlalchemy.DateTime(timezone=True), nullable=False)
)
