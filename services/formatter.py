from __future__ import annotations

from sources.base import Deal


class Formatter:

    @staticmethod
    def format_price(price: float | None) -> str:

        if price is None:
            return "-"

        return f"{price:,.2f} ₺".replace(",", ".")

    @classmethod
    def telegram(cls, deal: Deal, score: int) -> str:

        lines = []

        lines.append(f"🔥 <b>{deal.title}</b>")
        lines.append("")

        lines.append(f"💰 <b>{cls.format_price(deal.price)}</b>")

        if deal.old_price:
            lines.append(
                f"🏷️ Eski: {cls.format_price(deal.old_price)}"
            )

        if deal.discount:
            lines.append(
                f"📉 %{deal.discount} İndirim"
            )

        lines.append("")

        lines.append(
            f"🏪 {deal.retailer}"
        )

        if deal.seller:
            lines.append(
                f"🏬 Satıcı: {deal.seller}"
            )

        if deal.stock_count is not None:

            lines.append(
                f"📦 Stok: {deal.stock_count}"
            )

        elif deal.in_stock:

            lines.append(
                "📦 Stok: Var"
            )

        else:

            lines.append(
                "📦 Stok: Yok"
            )

        if deal.coupon:

            lines.append("")

            lines.append(
                f"🎟️ Kupon: {deal.coupon}"
            )

        lines.append("")

        lines.append(
            f"⭐ Fırsat Skoru: {score}/100"
        )

        lines.append("")

        lines.append(
            f"🛒 {deal.product_url}"
        )

        return "\n".join(lines)