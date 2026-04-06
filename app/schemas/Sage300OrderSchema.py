from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class OrderDetailSchema(BaseModel):
    """Represents a single line item in Sage 300 OrderDetails."""
    item: str = Field(..., alias="Item")
    qty_ordered: float = Field(..., alias="QuantityOrdered")
    unit_price: Optional[float] = Field(None, alias="UnitPrice")
    location: str = Field("1", alias="Location")
    uom: Optional[str] = Field(None, alias="UnitOfMeasure")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Sage300OrderSchema(BaseModel):
    """The main Sales Order payload for the OEOrders endpoint."""
    customer_number: str = Field(..., alias="CustomerNumber")
    purchase_order_number: Optional[str] = Field(None, alias="PurchaseOrderNumber")

    # Dates
    order_date: date = Field(default_factory=date.today, alias="OrderDate")
    expected_ship_date: Optional[date] = Field(None, alias="ExpectedShipDate")
    shipment_date: Optional[date] = Field(None, alias="ShipmentDate")

    # Delivery Address
    ship_to_name: Optional[str] = Field(None, alias="ShipToName")
    ship_to_address_line_1: Optional[str] = Field(None, alias="ShipToAddressLine1")
    ship_to_address_line_2: Optional[str] = Field(None, alias="ShipToAddressLine2")
    ship_to_city: Optional[str] = Field(None, alias="ShipToCity")
    ship_to_state: Optional[str] = Field(None, alias="ShipToStateProvince")
    ship_to_zip: Optional[str] = Field(None, alias="ShipToZipPostalCode")
    ship_to_country: Optional[str] = Field(None, alias="ShipToCountry")

    # Line Items
    order_details: List[OrderDetailSchema] = Field(default_factory=list, alias="OrderDetails")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d")}
    )
