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
    "Chrome/139.0.0.0 Safari/537.36"
)

# Discovery sadece buralardan başlar.
# Daha sonra yeni kaynaklar buraya eklenecek.
SEED_URLS = [
    "https://www.hepsiburada.com/",
    "https://www.hepsiburada.com/kampanyalar",
    "https://www.hepsiburada.com/cok-satanlar",
    "https://www.hepsiburada.com/yeni-gelen-urunler",
]

PRODUCT_RE = re.compile(
    r"https://www\.hepsiburada\.com/.+-p-[A-Za-z0-9]+/?$",
    re.IGNORECASE,
)


class HepsiburadaDiscovery(Discovery):

    @property
    def store(self):
        return "hepsiburada"

    def discover(self) -> Iterable[str]:

        session = requests.Session()

        session.headers.update({
            "User-Agent": USER_AGENT,
        })

        discovered = set()

        for seed in SEED_URLS:

            print(f"[DISCOVERY] {seed}")

            try:

                response = session.get(
                    seed,
                    timeout=30,
                )

                response.raise_for_status()

            except Exception as e:

                print(e)

                continue

            soup = BeautifulSoup(response.text, "lxml")

            for a in soup.find_all("a", href=True):

                href = urljoin(seed, a["href"])

                href = href.split("?")[0]

                href = href.rstrip("/")

                if PRODUCT_RE.match(href):
                    discovered.add(href)

        return sorted(discovered)