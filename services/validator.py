from __future__ import annotations

from dataclasses import dataclass

from services.rules import rules
from services.scoring import ScoringService
from sources.base import Deal


@dataclass(slots=True)
class ValidationResult:
    valid: bool
    score: int
    reasons: list[str]


class Validator:

    @staticmethod
    def validate(deal: Deal) -> ValidationResult:

        reasons: list[str] = []

        if not deal.product_url:
            return ValidationResult(
                False,
                0,
                ["Ürün linki bulunamadı."]
            )

        if rules.require_product_name and not deal.title:
            return ValidationResult(
                False,
                0,
                ["Ürün adı bulunamadı."]
            )

        if deal.price <= 0:
            return ValidationResult(
                False,
                0,
                ["Geçersiz fiyat."]
            )

        if rules.require_stock and not deal.in_stock:
            return ValidationResult(
                False,
                0,
                ["Stokta yok."]
            )

        if (
            deal.stock_count is not None
            and deal.stock_count < rules.minimum_stock
        ):
            return ValidationResult(
                False,
                0,
                [f"Stok {rules.minimum_stock} adetten az."]
            )

        score = ScoringService.calculate(deal)

        if score.score < rules.minimum_score:

            return ValidationResult(
                False,
                score.score,
                score.reasons,
            )

        return ValidationResult(
            True,
            score.score,
            score.reasons,
        )