from pydantic import BaseModel, ConfigDict


class OrderOcrExtractItem(BaseModel):
    product_supplier_code: str | None
    product_description: str | None
    quantity_ordered: float | None
    cost: float | None

    model_config = ConfigDict(from_attributes=True)
