from pydantic import BaseModel, ConfigDict
from datetime import date


class ProductCatalogSchema(BaseModel):
    customer: str | None
    date: date | None
    item: str | None
    product: str | None
    price: float | None
    ship_to_name: str | None
    # Addresses
    ship_to_address_1: str | None
    ship_to_address_2: str | None
    ship_to_address_3: str | None
    ship_to_address_4: str | None
    ship_to_city: str | None
    ship_to_state: str | None
    ship_to_zip: str | None
    ship_to_country: str | None

    model_config = ConfigDict(from_attributes=True)
