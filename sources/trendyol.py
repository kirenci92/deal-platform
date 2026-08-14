from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

import requests
from bs4 import BeautifulSoup

from sources.base import BaseSource, Deal
from sources.candidate import Candidate


class Trendyol(BaseSource):
    name = "Trendyol"

    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    )

    def _get(self, url: str) -> requests.Response:
        response = requests.get(
            url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
                ),
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
            },
            timeout=20,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _clean(value: Any) -> str | None:
        if value is None:
            return None

        value = str(value)
        value = re.sub(r"\s+", " ", value).strip()

        return value or None

    @staticmethod
    def _price(value: Any) -> float | None:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()

        text = re.sub(r"[^\d,.\-]", "", text)

        if not text:
            return None

        # Türkçe fiyat biçimi:
        # 1.299,99 -> 1299.99
        if "," in text and "." in text:
            text = text.replace(".", "").replace(",", ".")
        elif "," in text:
            text = text.replace(",", ".")
        elif text.count(".") > 1:
            text = text.replace(".", "")

        try:
            return float(text)
        except ValueError:
            return None

    @staticmethod
    def _jsonld(soup: BeautifulSoup) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []

        for script in soup.find_all(
            "script",
            attrs={"type": "application/ld+json"},
        ):
            raw = script.string or script.get_text(strip=True)

            if not raw:
                continue

            try:
                parsed = json.loads(raw)
            except (TypeError, json.JSONDecodeError):
                continue

            if isinstance(parsed, dict):
                data.append(parsed)

            elif isinstance(parsed, list):
                data.extend(
                    item for item in parsed
                    if isinstance(item, dict)
                )

        return data

    @staticmethod
    def _find_product_jsonld(
        items: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        for item in items:
            item_type = item.get("@type")

            if item_type == "Product":
                return item

            if isinstance(item_type, list) and "Product" in item_type:
                return item

            graph = item.get("@graph")

            if isinstance(graph, list):
                for node in graph:
                    if not isinstance(node, dict):
                        continue

                    node_type = node.get("@type")

                    if node_type == "Product":
                        return node

                    if (
                        isinstance(node_type, list)
                        and "Product" in node_type
                    ):
                        return node

        return None

    @staticmethod
    def _extract_discount(
        product: dict[str, Any],
        soup: BeautifulSoup,
    ) -> float | None:
        offers = product.get("offers")

        if isinstance(offers, dict):
            current = Trendyol._price(offers.get("price"))
            old = Trendyol._price(
                offers.get("highPrice")
                or offers.get("priceSpecification", {}).get(
                    "price"
                )
                if isinstance(
                    offers.get("priceSpecification"),
                    dict,
                )
                else None
            )

            if current is not None and old is not None and old > current:
                return round((old - current) / old * 100, 2)

        # Analyzer'da görülen indirim metinlerinden fallback.
        text = soup.get_text(" ", strip=True)

        match = re.search(
            r"%\s*(\d{1,3}(?:[.,]\d+)?)\s*(?:indirim|off)?",
            text,
            re.IGNORECASE,
        )

        if match:
            try:
                return float(match.group(1).replace(",", "."))
            except ValueError:
                pass

        return None

    def extract(self, candidate: Candidate) -> Deal | None:
        url = self._clean(getattr(candidate, "url", None))

        if not url:
            return None

        try:
            response = self._get(url)
        except requests.RequestException:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        jsonld_items = self._jsonld(soup)
        product = self._find_product_jsonld(jsonld_items)

        title: str | None = None
        image: str | None = None
        brand: str | None = None
        price: float | None = None
        old_price: float | None = None
        description: str | None = None

        if product:
            title = self._clean(product.get("name"))
            image_value = product.get("image")

            if isinstance(image_value, list):
                image = self._clean(image_value[0]) if image_value else None
            else:
                image = self._clean(image_value)

            description = self._clean(product.get("description"))

            brand_value = product.get("brand")

            if isinstance(brand_value, dict):
                brand = self._clean(brand_value.get("name"))
            else:
                brand = self._clean(brand_value)

            offers = product.get("offers")

            if isinstance(offers, dict):
                price = self._price(offers.get("price"))

                high_price = self._price(
                    offers.get("highPrice")
                )

                if (
                    high_price is not None
                    and price is not None
                    and high_price > price
                ):
                    old_price = high_price

        # JSON-LD bulunamazsa DOM fallback.
        if not title:
            meta = soup.find(
                "meta",
                attrs={"property": "og:title"},
            )
            if meta:
                title = self._clean(meta.get("content"))

        if not image:
            meta = soup.find(
                "meta",
                attrs={"property": "og:image"},
            )
            if meta:
                image = self._clean(meta.get("content"))

        if not description:
            meta = soup.find(
                "meta",
                attrs={"name": "description"},
            )
            if meta:
                description = self._clean(meta.get("content"))

        if price is None:
            price_selectors = [
                "[class*='price-current']",
                "[class*='current-price']",
                "[class*='product-price']",
                "[data-testid*='price']",
            ]

            for selector in price_selectors:
                element = soup.select_one(selector)

                if element:
                    price = self._price(
                        element.get_text(" ", strip=True)
                    )

                    if price is not None:
                        break

        if not title or price is None:
            return None

        discount = self._extract_discount(product or {}, soup)

        if old_price is None and discount and discount > 0:
            old_price = round(
                price / (1 - discount / 100),
                2,
            )

        deal_id = (
            self._clean(getattr(candidate, "id", None))
            or url
        )

        return Deal(
            id=deal_id,
            title=title,
            merchant="Trendyol",
            price=price,
            old_price=old_price,
            discount=discount,
            coupon=None,
            image=image,
            category=None,
            brand=brand,
            link=url,
            date=datetime.now(timezone.utc),
            description=description,
        )

    def get_deals(self) -> list[Deal]:
        return []


__all__ = ["Trendyol"]