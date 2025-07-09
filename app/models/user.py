from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class User(Base, UUIDMixin):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)

    client = relationship("Client", back_populates="users")
