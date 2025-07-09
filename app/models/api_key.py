from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class ApiKey(Base, UUIDMixin):
    __tablename__ = "api_keys"

    key = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="api_keys")
