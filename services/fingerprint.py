from __future__ import annotations

import hashlib

from sources.base import Deal


class FingerprintService:

    @staticmethod
    def generate(deal: Deal) -> str:
        """
        Aynı ürün için her zaman aynı fingerprint'i üretir.
        """

        values = [
            deal.retailer.strip().lower(),

            (deal.product_id or "").strip().lower(),

            deal.product_url.strip().lower(),

            (deal.brand or "").strip().lower(),
        ]

        raw = "|".join(values)

        return hashlib.sha256(raw.encode()).hexdigest()