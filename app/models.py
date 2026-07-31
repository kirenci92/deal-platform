from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(500))

    price: Mapped[float] = mapped_column(Float)

    old_price: Mapped[float] = mapped_column(Float)

    discount: Mapped[int]

    url: Mapped[str] = mapped_column(String(1000), unique=True)

    source: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
