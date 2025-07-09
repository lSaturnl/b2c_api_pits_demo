from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class Dispatch(Base, UUIDMixin):
    __tablename__ = "dispatches"

    dispatch_number = Column(String, nullable=False)
    pits_dispatch_id = Column(String, nullable=True)
    registered_at = Column(DateTime, nullable=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="dispatches")
    shipments = relationship("Shipment", back_populates="dispatch")
