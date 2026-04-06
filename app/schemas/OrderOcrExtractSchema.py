from typing import List, Optional
from app.schemas.OrderOcrExtractItemSchema import OrderOcrExtractItem
from pydantic import BaseModel, ConfigDict

# 1. Define the schema based on your Parseur Mailbox fields


class OrderOcrExtractSchema(BaseModel):
    buyer_email: Optional[str]
    buyer_name: Optional[str]
    buyer_phone: Optional[str]
    items: List[OrderOcrExtractItem]
    delivery_date: Optional[str]
    grand_total: Optional[float]
    supplier_name: Optional[str]
    customer_name: Optional[str]
    delivery_address: Optional[str]
    purchase_order_number: Optional[str]
    mail_box_id: Optional[str]

    model_config = ConfigDict(from_attributes=True)
