from sqlalchemy.orm import Session
from sqlalchemy import select, or_, text, func
from typing import List, Optional
from app.models.ProductCatalog import ProductCatalog
from app.database import get_db
from fastapi import Depends


class ProductRepository:
    DB_THRESHOLD = 0.1
    DB_RESULT_LIMIT = 5

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def _base_search(self, field, value, price: Optional[float] = None, code: Optional[str] = None,
                     description: Optional[str] = None):
        """Helper to reduce boilerplate in repository queries."""
        statement = (
            select(ProductCatalog)
            .distinct(ProductCatalog.item)
            .where(field.op("%")(value))
        )

        if price is not None:
            statement = statement.where(ProductCatalog.price == price)
        if code:
            statement = statement.where(ProductCatalog.item == code)
        if description:
            statement = statement.where(ProductCatalog.product.op("%")(description))

        statement = statement.order_by(
            ProductCatalog.item,
            field.op("<->")(value)
        )
        # statement.limit(self.DB_RESULT_LIMIT)
        self.db.execute(text(f"SET pg_trgm.similarity_threshold = {self.DB_THRESHOLD};"))
        return self.db.execute(statement).scalars().all()

    def get_products_by_customer_and_price(self, customer_name: Optional[str], address: Optional[str], price: float)\
            -> List[ProductCatalog]:
        results = []
        if customer_name and customer_name.strip():
            results = self._base_search(ProductCatalog.customer, customer_name.strip(), price=price)

        if not results and address and address.strip():
            results = self._base_search(ProductCatalog.ship_to_address_1, address.strip(), price=price)

        return list(results)

    def get_products_by_product_code(self, customer_name: str, address: str, code: str) -> List[ProductCatalog]:
        # Implementation mirrors logic: check customer, then fallback to address
        self.db.execute(text(f"SET pg_trgm.similarity_threshold = {0.3};"))
        results = self._base_search(ProductCatalog.customer, customer_name.strip(), code=code) if customer_name.strip() else []
        # print(f"given customer: {customer_name}")
        if not results and address and address.strip():
            results = self._base_search(ProductCatalog.ship_to_address_1, address.strip(), code=code)

        return list(results)

    def get_products_by_description(self, customer_name: str, address: str, description: str) -> List[ProductCatalog]:
        results = self._base_search(ProductCatalog.customer, customer_name.strip(),
                                    description=description) if customer_name else []
        if not results and address and address.strip():
            results = self._base_search(ProductCatalog.ship_to_address_1, address.strip(), description=description)
        return list(results)

    def get_by_id(self, product_id: int) -> Optional[ProductCatalog]:
        """Fetch a single record by its primary key."""
        return self.db.get(ProductCatalog, product_id)

    def create_product(self, data: dict) -> ProductCatalog:
        """Standard method to insert a new catalog entry."""
        new_product = ProductCatalog(**data)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_ship_to_address(self, delivery_address: str, customer_name: Optional[str] = None) -> ProductCatalog:
        extract_address_from: ProductCatalog = ProductCatalog()
        address = delivery_address.replace("-", " ").replace(",", "")
        search_term = address
        # " ".join(address.split()[:4]).upper()
        # print(f"using search term {search_term}")
        # 1. Start with base address conditions
        conditions = [
            ProductCatalog.ship_to_address_1.op("%")(search_term),
            ProductCatalog.ship_to_address_2.op("%")(search_term)
        ]

        # 2. Add the customer condition ONLY if it's available
        if customer_name:
            conditions.append(ProductCatalog.customer.op("%")(customer_name.strip()))

        combined_address = (
                func.coalesce(ProductCatalog.ship_to_address_1, '') + " " +
                func.coalesce(ProductCatalog.ship_to_address_2, '')
        )
        statement = select(ProductCatalog).where(
            or_(*conditions)
        ).order_by(
            combined_address.op("<->")(search_term)
        )
        statement.limit(self.DB_RESULT_LIMIT)

        self.db.execute(text(f"SET pg_trgm.similarity_threshold = {self.DB_THRESHOLD};"))
        results = self.db.execute(statement).scalars().all()
        if results:
            extract_address_from = results[0]
            return extract_address_from

        return extract_address_from
