from __future__ import annotations

from dataclasses import dataclass

from services.rules import rules
from sources.base import Deal


@dataclass(slots=True)
class ScoreResult:
    score: int
    reasons: list[str]


class ScoringService:

    @staticmethod
    def calculate(deal: Deal) -> ScoreResult:

        score = 0
        reasons: list[str] = []

        # Stok
        if deal.in_stock:
            score += 25
            reasons.append("+25 Stok mevcut")
        else:
            reasons.append("Stok yok")

        # Kalan stok
        if deal.stock_count is not None:
            if deal.stock_count >= 10:
                score += 10
                reasons.append("+10 Yüksek stok")

            elif deal.stock_count >= 5:
                score += 5
                reasons.append("+5 Orta stok")

            elif deal.stock_count == 1:
                score -= 5
                reasons.append("-5 Son ürün")

        # İndirim

        if deal.discount is not None:

            if deal.discount >= 50:
                score += 35
                reasons.append("+35 %50+ indirim")

            elif deal.discount >= 30:
                score += 25
                reasons.append("+25 %30+ indirim")

            elif deal.discount >= rules.minimum_discount:
                score += 15
                reasons.append("+15 İndirim")

        # Kupon

        if deal.coupon:
            score += 10
            reasons.append("+10 Kupon")

        # Mağaza

        trusted = {
            "Amazon": 20,
            "Hepsiburada": 20,
            "Trendyol": 18,
            "Pazarama": 18,
            "Teknosa": 18,
            "MediaMarkt": 20,
            "N11": 15,
        }

        score += trusted.get(deal.retailer, 10)

        reasons.append(
            f"+{trusted.get(deal.retailer,10)} {deal.retailer}"
        )

        return ScoreResult(
            score=score,
            reasons=reasons,
        )