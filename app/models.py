from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects import postgresql

from app.db import Base


class NodeModel(Base):
    __tablename__ = "tree"

    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    parent_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("tree.id"), nullable=True
    )
    title: str = Column(String(60), nullable=False)
    registered_in: datetime = Column(
        DateTime(), default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"Node <{self.title}>"
