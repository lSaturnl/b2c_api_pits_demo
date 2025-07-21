from sqlalchemy import Column, BigInteger
from app.models.base import Base  # або просто Base, якщо не використовуєш модульну структуру

class ParcelNumberCounter(Base):
    __tablename__ = "parcel_number_counter"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    current = Column(BigInteger, nullable=False)
