from sqlalchemy import Column, String, Integer, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class ShipmentItem(Base, UUIDMixin):
    __tablename__ = "shipment_items"

    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)

    name = Column(String)
    brand = Column(String)
    quantity = Column(Integer)
    weight = Column(Numeric)
    value = Column(Numeric)
    value_currency = Column(String)
    hs_code = Column(String)
    notes = Column(Text)

    shipment = relationship("Shipment", back_populates="items")
