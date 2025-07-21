from sqlalchemy.orm import Session
from app.models.parcel_number_counter import ParcelNumberCounter
from uuid import uuid4

def calculate_check_digit_full(number: str) -> str:
    """Контрольна цифра для повного 12-значного номера"""
    weights = [8, 6, 4, 2, 3, 5, 9, 7, 8, 6, 4, 2]
    total = sum(int(d) * w for d, w in zip(number, weights))
    remainder = total % 11
    result = 11 - remainder
    if result == 10:
        return '0'
    elif result == 11:
        return '5'
    return str(result)


def generate_parcel_number(db: Session, prefix: str = "CV", country_code: str = "UA", base: int = 2142000000000) -> str:
    counter = db.query(ParcelNumberCounter).first()
    if not counter:
        counter = ParcelNumberCounter(current=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)

    numeric_part = str(int(base) + int(counter.current))
    check_digit = calculate_check_digit_full(numeric_part)

    counter.current += 1
    db.commit()

    return f"{prefix}{numeric_part}{check_digit}{country_code}"
