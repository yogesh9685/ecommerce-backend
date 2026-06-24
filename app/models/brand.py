from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.base import Base


class Brand(Base):
    __tablename__ = "brands"

    name = Column(String(150), nullable=False, unique=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(512), nullable=True)
    website_url = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="brand")
