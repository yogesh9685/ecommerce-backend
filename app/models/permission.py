from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
