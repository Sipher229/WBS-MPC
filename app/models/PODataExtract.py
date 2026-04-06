from __future__ import annotations
from typing import List, TYPE_CHECKING
from typing import Optional
from app.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, DateTime


if TYPE_CHECKING:
    from app.models.DocumentTracker import DocumentTracker


class PODataExtract(Base):
    __tablename__ = "purchase_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[str]  # Or use a Date/DateTime type
    description: Mapped[Optional[str]]
    buyer_email: Mapped[Optional[str]]
    buyer_name: Mapped[Optional[str]]
    buyer_phone: Mapped[Optional[str]]
    document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("document_tracker.document_id"))
    # Establishes the one-to-many relationship
    # 'items' will be a list of POItem objects associated with this PO
    items: Mapped[Optional[List["PODataExtractItem"]]] = relationship(back_populates="purchase_order", cascade="all, delete-orphan")
    delivery_date: Mapped[Optional[str]]
    grand_total: Mapped[Optional[float]]
    supplier_name: Mapped[Optional[str]]
    customer_name: Mapped[Optional[str]]
    delivery_address: Mapped[Optional[str]]
    purchase_order_number: Mapped[Optional[str]]
    mail_box_id: Mapped[Optional[str]]
    document: Mapped[DocumentTracker] = relationship(back_populates="extracted_data")

    def __repr__(self) -> str:
        return f"PurchaseOrder(id={self.id!r}, description={self.description!r})"


class PODataExtractItem(Base):
    __tablename__ = "po_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    po_id: Mapped[int] = mapped_column(ForeignKey("purchase_order.id"))
    product_supplier_code: Mapped[Optional[str]]
    product_description: Mapped[Optional[str]]
    quantity_ordered: Mapped[Optional[float]]
    cost: Mapped[Optional[float]]

    # Establishes the many-to-one relationship (reverse side)
    # 'purchase_order' will be a single PurchaseOrder object
    purchase_order: Mapped["PODataExtract"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"POItem(id={self.id!r}, product_code={self.product_supplier_code!r}, quantity={self.quantity_ordered!r})"



