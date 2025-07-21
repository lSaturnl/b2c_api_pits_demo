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
        # Генеруємо parcel_number (в нас він зберігається як tracking_number)
        tracking_number = generate_parcel_number(db)

        new_shipment = Shipment(
            receiver_name=data.recipient_name,
            receiver_street_id=None,  # або витягати з recipient_address (розпарсити)
            receiver_house=None,      # те саме
            receiver_city_id=None,
            receiver_area_id=None,
            receiver_zip=None,
            receiver_phone="380000000000",  # можна тимчасово хардкодити або передавати окремо
            tracking_number=tracking_number,
            client_id=data.client_id,
        )
        db.add(new_shipment)
        db.flush()

        for item in data.items:
            db.add(ShipmentItem(
                shipment_id=new_shipment.id,
                name=item.name,
                brand=item.brand,
                quantity=item.quantity,
                weight=item.weight,
                value=item.value,
                value_currency=item.value_currency,
                hs_code=item.hs_code,
                notes=item.notes
            ))
        result.append(new_shipment)

    db.commit()
    return result
