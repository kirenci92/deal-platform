from __future__ import annotations

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Deal as DealModel
from sources.base import Deal


class DatabaseService:

    @staticmethod
    def exists(fingerprint: str) -> bool:

        db = SessionLocal()

        try:

            return (
                db.scalar(
                    select(DealModel).where(
                        DealModel.fingerprint == fingerprint
                    )
                )
                is not None
            )

        finally:

            db.close()

    @staticmethod
    def save(deal: Deal):

        db = SessionLocal()

        try:

            db.add(
                DealModel(
                    fingerprint=deal.fingerprint,
                    product_id=deal.product_id,
                    title=deal.title,
                    retailer=deal.retailer,
                    seller=deal.seller,
                    url=deal.product_url,
                    image_url=deal.image_url,
                    brand=deal.brand,
                    category=deal.category,
                    price=deal.price,
                    old_price=deal.old_price,
                    discount=deal.discount,
                    coupon=deal.coupon,
                    in_stock=deal.in_stock,
                    stock_count=deal.stock_count,
                    discovery_source=deal.discovery_source,
                )
            )

            db.commit()

        finally:

            db.close()
