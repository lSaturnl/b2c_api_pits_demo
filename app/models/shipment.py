from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class Shipment(Base, UUIDMixin):
    __tablename__ = "shipments"

    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    dispatch_id = Column(UUID(as_uuid=True), ForeignKey("dispatches.id"), nullable=True)

    tracking_number = Column(String, unique=True, nullable=True)
    order_number = Column(String, nullable=True)

    receiver_name = Column(String)
    receiver_phone = Column(String)
    receiver_country = Column(String)
    receiver_area_id = Column(String)
    receiver_city_id = Column(String)
    receiver_street_id = Column(String)
    receiver_house = Column(String)
    receiver_flat = Column(String)
    receiver_zip = Column(String)
    receiver_branch_id = Column(String)
    receiver_branch_name = Column(String)
    receiver_branch_number = Column(String)

    weight = Column(Numeric)
    length = Column(Numeric)
    width = Column(Numeric)
    height = Column(Numeric)

    declared_value = Column(Numeric)
    value_currency = Column(String)
    service_type = Column(String)
    is_cod = Column(Boolean, default=False)
    cod_amount = Column(Numeric)
    label_path = Column(String)

    client = relationship("Client", back_populates="shipments")
    dispatch = relationship("Dispatch", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment", cascade="all, delete-orphan")
    statuses = relationship("ShipmentStatus", back_populates="shipment", cascade="all, delete-orphan")
