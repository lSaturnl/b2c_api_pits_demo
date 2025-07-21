from sqlalchemy.orm import Session
from app.models.parcel_number_counter import ParcelNumberCounter

def generate_parcel_number(db: Session) -> str:
    counter = db.query(ParcelNumberCounter).first()
    if not counter:
        raise ValueError("ParcelNumberCounter not initialized")

    current = counter.current + 1
    counter.current = current
    db.commit()

    return f"CV{current:09d}UA"
