from __future__ import annotations

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Deal as DealModel
from sources.base import Deal


class DedupService:

    @staticmethod
    def exists(deal: Deal) -> bool:

        db = SessionLocal()

        try:

            if deal.fingerprint:

                found = db.scalar(
                    select(DealModel).where(
                        DealModel.fingerprint == deal.fingerprint
                    )
                )

                if found:
                    return True

            found = db.scalar(
                select(DealModel).where(
                    DealModel.url == deal.product_url
                )
            )

            return found is not None

        finally:
            db.close()
