from pydantic import BaseModel
from typing import List

class ShipmentItemCreate(BaseModel):
    description: str
    weight: float
    quantity: int

class ShipmentCreate(BaseModel):
    recipient_name: str
    recipient_address: str
    client_id: str
    dispatch_id: str
    items: List[ShipmentItemCreate]

class ShipmentResponse(BaseModel):
    id: str
    recipient_name: str
    recipient_address: str
    parcel_number: str

    class Config:
        orm_mode = True
