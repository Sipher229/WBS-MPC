from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Date
from datetime import date
from app.database import Base


class ProductCatalog(Base):
    __tablename__ = "product_catalog"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_number: Mapped[int] = mapped_column(Integer, nullable=True)
    invoice_number: Mapped[str] = mapped_column(String, nullable=True)
    customer_po_number: Mapped[str] = mapped_column(String, nullable=True)
    qty_ord: Mapped[int] = mapped_column(Integer, nullable=True)
    customer: Mapped[str] = mapped_column(String)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    item: Mapped[str] = mapped_column(String)
    product: Mapped[str] = mapped_column(String)
    uom: Mapped[str] = mapped_column(String)  # Unit of Measure
    price: Mapped[float] = mapped_column(Float)
    ship_to_name: Mapped[str] = mapped_column(String, nullable=True)
    # Addresses
    ship_to_address_1: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_address_2: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_address_3: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_address_4: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_city: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_state: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_zip: Mapped[str] = mapped_column(String, nullable=True)
    ship_to_country: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"POItem(id={self.id!r}, customer={self.customer!r}, product={self.product!r}),\
         ship_to_address_1={self.ship_to_address_1!r}"

