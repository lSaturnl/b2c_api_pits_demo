#app/models/client_tariff.py
from sqlalchemy import Column, Numeric, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin

class ClientTariff(Base, UUIDMixin):
    __tablename__ = "client_tariffs"

    client_id = Column(ForeignKey("clients.id"), nullable=False)

    min_weight = Column(Numeric, nullable=False)
    max_weight = Column(Numeric, nullable=True)  # null означає "немає верхньої межі"
    price_per_kg = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False, default="UAH")

    client = relationship("Client", back_populates="tariffs")
