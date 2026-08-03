from app.database import Base, SessionLocal, engine
from app.models import Deal as DealModel
from app.telegram import Telegram

from services.dedup import DedupService
from services.fingerprint import FingerprintService
from services.formatter import Formatter
from services.validator import Validator

from sources.base import BaseSource, Deal
from sources.dh import DonanimHaber


class DealPlatform:

    def __init__(self):

        Base.metadata.create_all(bind=engine)

        self.sources: list[BaseSource] = [
            DonanimHaber(),
        ]

    def run(self):

        print("=" * 60)
        print(" Deal Platform v1.0")
        print("=" * 60)

        for source in self.sources:

            print(f"\nKaynak: {source.name}")

            deals = source.get_deals()

            print(f"{len(deals)} fırsat bulundu.")

            for deal in deals:

                deal.fingerprint = FingerprintService.generate(
                    deal
                )

                if DedupService.exists(deal):
                    continue

                result = Validator.validate(deal)

                if not result.valid:

                    print(
                        f"Reddedildi: {result.reasons}"
                    )

                    continue

                message = Formatter.telegram(
                    deal,
                    result.score,
                )

                if Telegram.send(message):

                    self.save(deal)

                    print(
                        f"Gönderildi: {deal.title}"
                    )

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


if __name__ == "__main__":
    DealPlatform().run()