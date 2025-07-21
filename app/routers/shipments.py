from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.models.shipment_item import ShipmentItem
from app.db import get_db
from app.schemas.shipment import ShipmentCreate, ShipmentResponse
from app.utils.parcel_number import generate_parcel_number

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.post("/", response_model=list[ShipmentResponse])
def create_shipments(shipments: list[ShipmentCreate], db: Session = Depends(get_db)):
    result = []
    for data in shipments:
        # Генеруємо новий parcel_number
        parcel_number = generate_parcel_number(db)

        new_shipment = Shipment(
            recipient_name=data.recipient_name,
            recipient_address=data.recipient_address,
            parcel_number=parcel_number,
            client_id=data.client_id,
            dispatch_id=data.dispatch_id,
        )
        db.add(new_shipment)
        db.flush()  # Щоб отримати ID

        for item in data.items:
            db.add(ShipmentItem(
                shipment_id=new_shipment.id,
                description=item.description,
                weight=item.weight,
                quantity=item.quantity
            ))
        result.append(new_shipment)
    db.commit()
    return result
