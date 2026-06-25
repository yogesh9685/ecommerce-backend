from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    avatar_url = Column(String(512), nullable=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    orders = relationship("Order", back_populates="user")
    cart_items = relationship(
        "CartItem", back_populates="user", cascade="all, delete-orphan"
    )
    wishlist_items = relationship(
        "WishlistItem", back_populates="user", cascade="all, delete-orphan"
    )
    reviews = relationship("Review", back_populates="user")
