from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from sources.base import BaseSource, Deal


class DonanimHaber(BaseSource):

    name = "DonanimHaber"

    URL = "https://forum.donanimhaber.com/sicak-firsatlar--f193"

    HEADERS = {
        "User-Agent":
            "Mozilla/5.0"
    }

    STORE_PATTERNS = {
        "amazon": "Amazon",
        "hepsiburada": "Hepsiburada",
        "trendyol": "Trendyol",
        "n11": "N11",
        "mediamarkt": "MediaMarkt",
        "teknosa": "Teknosa",
        "pazarama": "Pazarama",
    }

    def get_deals(self) -> list[Deal]:

        response = requests.get(
            self.URL,
            headers=self.HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        deals: list[Deal] = []

        links = soup.find_all("a", href=True)

        for a in links:

            href = a["href"]

            if not href.startswith("http"):
                continue

            retailer = None

            for key, value in self.STORE_PATTERNS.items():

                if key in href.lower():
                    retailer = value
                    break

            if retailer is None:
                continue

            deals.append(
                Deal(
                    title="",
                    product_url=href,
                    retailer=retailer,
                    price=0,
                    discovery_source="DonanimHaber",
                )
            )

        unique = []

        seen = set()

        for deal in deals:

            if deal.product_url in seen:
                continue

            seen.add(deal.product_url)

            unique.append(deal)

        return unique