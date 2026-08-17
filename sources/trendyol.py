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
                    "application/xml;q=0.9,image/avif,image/webp,"
                    "*/*;q=0.8"
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
                    item
                    for item in parsed
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

            if (
                isinstance(item_type, list)
                and "Product" in item_type
            ):
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
    ) -> int | None:
        offers = product.get("offers")

        if isinstance(offers, dict):
            current = Trendyol._price(
                offers.get("price")
            )

            price_specification = offers.get(
                "priceSpecification"
            )

            specification_price = None

            if isinstance(price_specification, dict):
                specification_price = Trendyol._price(
                    price_specification.get("price")
                )

            high_price = Trendyol._price(
                offers.get("highPrice")
            )

            old = high_price or specification_price

            if (
                current is not None
                and old is not None
                and old > current
            ):
                return round(
                    (old - current) / old * 100
                )

        # Analyzer'da görülen indirim metinlerinden fallback.
        text = soup.get_text(" ", strip=True)

        match = re.search(
            r"%\s*(\d{1,3}(?:[.,]\d+)?)"
            r"\s*(?:indirim|off)?",
            text,
            re.IGNORECASE,
        )

        if match:
            try:
                return round(
                    float(
                        match.group(1).replace(",", ".")
                    )
                )
            except ValueError:
                pass

        return None

    @staticmethod
    def _extract_product_id(
        product: dict[str, Any],
    ) -> str | None:
        return (
            Trendyol._clean(product.get("sku"))
            or Trendyol._clean(product.get("mpn"))
        )

    @staticmethod
    def _extract_seller(
        offers: dict[str, Any] | None,
    ) -> str | None:
        if not isinstance(offers, dict):
            return None

        seller = offers.get("seller")

        if isinstance(seller, dict):
            return Trendyol._clean(
                seller.get("name")
            )

        return Trendyol._clean(seller)

    @staticmethod
    def _extract_stock(
        offers: dict[str, Any] | None,
    ) -> bool:
        if not isinstance(offers, dict):
            return True

        availability = Trendyol._clean(
            offers.get("availability")
        )

        if not availability:
            return True

        availability = availability.lower()

        if "outofstock" in availability:
            return False

        if "soldout" in availability:
            return False

        if "instock" in availability:
            return True

        return True

    @staticmethod
    def _discovered_at(
        candidate: Candidate,
    ) -> datetime:
        value = getattr(
            candidate,
            "discovered_at",
            None,
        )

        if isinstance(value, datetime):
            return value

        if isinstance(value, str) and value.strip():
            try:
                parsed = datetime.fromisoformat(
                    value.replace("Z", "+00:00")
                )

                if parsed.tzinfo is None:
                    return parsed.replace(
                        tzinfo=timezone.utc
                    )

                return parsed
            except ValueError:
                pass

        return datetime.now(timezone.utc)

    def extract(
        self,
        candidate: Candidate,
    ) -> Deal | None:
        url = self._clean(
            getattr(candidate, "merchant_url", None)
        )

        if not url:
            return None

        try:
            response = self._get(url)
        except requests.RequestException:
            return None

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

        jsonld_items = self._jsonld(soup)
        product = self._find_product_jsonld(
            jsonld_items
        )

        title: str | None = None
        image: str | None = None
        brand: str | None = None
        price: float | None = None
        old_price: float | None = None
        description: str | None = None
        product_id: str | None = None
        seller: str | None = None
        in_stock = True

        offers: dict[str, Any] | None = None

        if product:
            title = self._clean(
                product.get("name")
            )

            image_value = product.get("image")

            if isinstance(image_value, list):
                image = (
                    self._clean(image_value[0])
                    if image_value
                    else None
                )
            else:
                image = self._clean(image_value)

            description = self._clean(
                product.get("description")
            )

            brand_value = product.get("brand")

            if isinstance(brand_value, dict):
                brand = self._clean(
                    brand_value.get("name")
                )
            else:
                brand = self._clean(brand_value)

            product_id = self._extract_product_id(
                product
            )

            product_offers = product.get("offers")

            if isinstance(product_offers, dict):
                offers = product_offers

                price = self._price(
                    offers.get("price")
                )

                high_price = self._price(
                    offers.get("highPrice")
                )

                price_specification = offers.get(
                    "priceSpecification"
                )

                specification_price = None

                if isinstance(
                    price_specification,
                    dict,
                ):
                    specification_price = (
                        self._price(
                            price_specification.get(
                                "price"
                            )
                        )
                    )

                old_candidate = (
                    high_price
                    or specification_price
                )

                if (
                    old_candidate is not None
                    and price is not None
                    and old_candidate > price
                ):
                    old_price = old_candidate

                seller = self._extract_seller(
                    offers
                )

                in_stock = self._extract_stock(
                    offers
                )

        # JSON-LD bulunamazsa DOM fallback.
        if not title:
            meta = soup.find(
                "meta",
                attrs={"property": "og:title"},
            )

            if meta:
                title = self._clean(
                    meta.get("content")
                )

        if not image:
            meta = soup.find(
                "meta",
                attrs={"property": "og:image"},
            )

            if meta:
                image = self._clean(
                    meta.get("content")
                )

        if not description:
            meta = soup.find(
                "meta",
                attrs={"name": "description"},
            )

            if meta:
                description = self._clean(
                    meta.get("content")
                )

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
                        element.get_text(
                            " ",
                            strip=True,
                        )
                    )

                    if price is not None:
                        break

        if not title or price is None:
            return None

        discount = self._extract_discount(
            product or {},
            soup,
        )

        if old_price is None and discount and discount > 0:
            calculated_old_price = price / (
                1 - discount / 100
            )

            old_price = round(
                calculated_old_price,
                2,
            )

        retailer = (
            self._clean(
                getattr(candidate, "retailer", None)
            )
            or self.name
        )

        discovery_source = self._clean(
            getattr(
                candidate,
                "discovery_source",
                None,
            )
        )

        return Deal(
            title=title,
            product_url=url,
            retailer=retailer,
            price=price,
            old_price=old_price,
            discount=discount,
            coupon=None,
            image_url=image,
            brand=brand,
            category=None,
            seller=seller,
            in_stock=in_stock,
            stock_count=None,
            product_id=product_id,
            fingerprint=None,
            discovery_source=discovery_source,
            discovered_at=self._discovered_at(
                candidate
            ),
        )

    def get_deals(self) -> list[Deal]:
        return []


__all__ = ["Trendyol"]