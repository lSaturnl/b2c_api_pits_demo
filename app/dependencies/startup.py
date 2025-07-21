from app.db import SessionLocal
from app.models import ParcelNumberCounter

def init_parcel_number_counter():
    db = SessionLocal()
    if not db.query(ParcelNumberCounter).first():
        db.add(ParcelNumberCounter(current=2142002755066))
        db.commit()
    db.close()
