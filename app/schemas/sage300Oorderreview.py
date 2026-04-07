from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date


class OrderDetailReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Original Data
    item: Optional[str] = None  # product code
    qty_ordered: Optional[float] = Field(0, description="The quantity requested for this item")
    unit_price: Optional[float] = None
    location: str = "1"
    uom: Optional[str] = None

    # Normalisation Metadata
    original_description: Optional[str] = Field(None, description="The raw description from the doc")
    suggested_item_code: Optional[str] = Field(None, description="The code found by fuzzy match")
    match_score: float = Field(0.0, ge=0, le=100)
    needs_review: bool = False
    review_reason: Optional[str] = None


class OrderHeaderReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_number: str
    purchase_order_number: Optional[str] = None
    order_date: date
    expected_ship_date: Optional[date] = None

    # Address Info
    ship_to_name: Optional[str] = None
    ship_to_address_line_1: Optional[str] = None
    ship_to_address_line_2: Optional[str] = None
    ship_to_city: Optional[str] = None

    # The Review Logic
    is_fully_normalized: bool = Field(
        False,
        description="True only if all lines passed the confidence threshold"
    )
    total_items_needing_review: int = 0

    # Nested Line Items
    order_details: List[OrderDetailReview]
