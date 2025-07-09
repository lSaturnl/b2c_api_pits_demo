from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, UUIDMixin

class ShipmentStatus(Base, UUIDMixin):
    __tablename__ = "shipment_statuses"

    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)

    status_code = Column(String)
    status_text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)

    shipment = relationship("Shipment", back_populates="statuses")
