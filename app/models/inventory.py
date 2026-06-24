from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    warehouse_location = Column(String(100), nullable=True)

    product = relationship("Product", back_populates="inventory")

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity
