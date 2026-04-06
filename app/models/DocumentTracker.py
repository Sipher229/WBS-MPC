from typing import List, TYPE_CHECKING
from typing import Optional
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, func
from app.models.PODataExtract import PODataExtract
from datetime import datetime
from app.utils.DocumentState import DocumentState


class DocumentTracker(Base):
    __tablename__ = "document_tracker"

    document_id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    status: Mapped[str] = mapped_column(default=DocumentState.PENDING)
    filename: Mapped[str]
    extracted_data: Mapped[Optional["PODataExtract"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"Document(id={self.document_id!r}, description={self.status!r}), extracted_data={self.extracted_data}"

