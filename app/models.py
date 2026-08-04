from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)

    fingerprint: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    product_id: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
    )

    retailer: Mapped[str] = mapped_column(
        String(80),
    )

    seller: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    url: Mapped[str] = mapped_column(
        String(1200),
        unique=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(1200),
        nullable=True,
    )

    brand: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    price: Mapped[float] = mapped_column(Float)

    old_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    discount: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    coupon: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    prime: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    event_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    event_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    stock_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    discovery_source: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )