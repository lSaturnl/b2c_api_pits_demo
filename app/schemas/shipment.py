from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ShipmentItemCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    quantity: int
    weight: float
    value: Optional[float] = None
    value_currency: Optional[str] = None
    hs_code: Optional[str] = None
    notes: Optional[str] = None

class ShipmentCreate(BaseModel):
    recipient_name: str
    recipient_address: str
    client_id: str
    dispatch_id: Optional[str] = None
    items: List[ShipmentItemCreate]

class ShipmentResponse(BaseModel):
    id: UUID
    receiver_name: str
    receiver_city_id: Optional[str] = None  # або інше, якщо треба
    tracking_number: Optional[str] = None

    class Config:
        orm_mode = True
