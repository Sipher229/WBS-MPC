from datetime import date
from typing import List, Optional
from sqlalchemy import String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database import Base


class OrderHeader(Base):
    """The main Sales Order table (Header)."""
    __tablename__ = "order_headers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_number: Mapped[str] = mapped_column(String(20), nullable=False)
    purchase_order_number: Mapped[Optional[str]] = mapped_column(String(50))

    # Dates (Stored as actual Date objects)
    order_date: Mapped[date] = mapped_column(Date, default=date.today)
    expected_ship_date: Mapped[Optional[date]] = mapped_column(Date)
    shipment_date: Mapped[Optional[date]] = mapped_column(Date)

    # Delivery Address
    ship_to_name: Mapped[Optional[str]] = mapped_column(String(100))
    ship_to_address_line_1: Mapped[Optional[str]] = mapped_column(String(100))
    ship_to_address_line_2: Mapped[Optional[str]] = mapped_column(String(100))
    ship_to_city: Mapped[Optional[str]] = mapped_column(String(50))
    ship_to_state: Mapped[Optional[str]] = mapped_column(String(50))
    ship_to_zip: Mapped[Optional[str]] = mapped_column(String(20))
    ship_to_country: Mapped[Optional[str]] = mapped_column(String(50))

    # Relationship to Line Items
    order_details: Mapped[List["OrderDetail"]] = relationship(
        back_populates="header", cascade="all, delete-orphan", lazy="selectin"
    )


class OrderDetail(Base):
    """The individual line items for an order (Details)."""
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    header_id: Mapped[int] = mapped_column(ForeignKey("order_headers.id"))

    item: Mapped[str] = mapped_column(String(50), nullable=False)
    qty_ordered: Mapped[float] = mapped_column(Float, default=0.0)
    unit_price: Mapped[Optional[float]] = mapped_column(Float)
    location: Mapped[str] = mapped_column(String(10), default="1")
    uom: Mapped[Optional[str]] = mapped_column(String(10))  # Unit of Measure

    # Back-reference to the Header
    header: Mapped["OrderHeader"] = relationship(back_populates="order_details")
