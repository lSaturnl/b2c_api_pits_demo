from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class Client(Base, UUIDMixin):
    __tablename__ = "clients"

    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    company_name = Column(String, nullable=True)

    api_keys = relationship("ApiKey", back_populates="client")
    users = relationship("User", back_populates="client")
    shipments = relationship("Shipment", back_populates="client")
    dispatches = relationship("Dispatch", back_populates="client")
    tariffs = relationship("ClientTariff", back_populates="client", cascade="all, delete-orphan")
