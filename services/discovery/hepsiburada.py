import re
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from services.discovery.base import Discovery


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/139.0 Safari/537.36"
)


SEED_URLS = [
    "https://www.hepsiburada.com/kampanyalar",
    "https://www.hepsiburada.com/",
]


PRODUCT_PATTERN = re.compile(
    r"^https://www\.hepsiburada\.com/.+-p-[A-Z0-9]+/?$",
    re.IGNORECASE,
)


class HepsiburadaDiscovery(Discovery):

    @property
    def store(self) -> str:
        return "hepsiburada"

    def discover(self) -> Iterable[str]:

        found = set()

        session = requests.Session()

        session.headers.update({
            "User-Agent": USER_AGENT,
        })

        for seed in SEED_URLS:

            try:
                response = session.get(
                    seed,
                    timeout=30,
                )

                response.raise_for_status()

            except Exception:
                continue

            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all("a", href=True):

                href = urljoin(seed, link["href"])

                href = href.split("?")[0]

                if PRODUCT_PATTERN.match(href):
                    found.add(href.rstrip("/"))

        return sorted(found)
