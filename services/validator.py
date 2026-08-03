from __future__ import annotations

from sources.base import Deal


class ValidationResult:
    def __init__(self, valid: bool, reason: str = ""):
        self.valid = valid
        self.reason = reason


class Validator:

    MIN_DISCOUNT = 10

    @classmethod
    def validate(cls, deal: Deal) -> ValidationResult:

        if not deal.product_url:
            return ValidationResult(False, "Ürün linki yok.")

        if not deal.title:
            return ValidationResult(False, "Ürün adı yok.")

        if deal.price <= 0:
            return ValidationResult(False, "Geçersiz fiyat.")

        if not deal.in_stock:
            return ValidationResult(False, "Stokta yok.")

        if (
            deal.old_price
            and deal.old_price <= deal.price
        ):
            return ValidationResult(
                False,
                "Eski fiyat güncel fiyattan düşük."
            )

        if (
            deal.discount is not None
            and deal.discount < cls.MIN_DISCOUNT
        ):
            return ValidationResult(
                False,
                f"İndirim %{cls.MIN_DISCOUNT} altında."
            )

        return ValidationResult(True)