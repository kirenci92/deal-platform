import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from services.discovery.base import Discovery
from services.discovery.url_filter import filter_urls


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/139.0.0.0 Safari/537.36"
)


SEED_URLS = [
    "https://www.hepsiburada.com/",
    "https://www.hepsiburada.com/kampanyalar",
    "https://www.hepsiburada.com/cok-satanlar",
    "https://www.hepsiburada.com/yeni-gelen-urunler",
]


class HepsiburadaDiscovery(Discovery):

    @property
    def store(self):
        return "hepsiburada"

    def discover(self):

        session = requests.Session()

        session.headers.update({
            "User-Agent": USER_AGENT,
        })

        urls = []

        for seed in SEED_URLS:

            print(f"[DISCOVERY] {seed}")

            try:

                response = session.get(
                    seed,
                    timeout=30,
                )

                response.raise_for_status()

            except Exception as exc:

                print(exc)

                continue

            soup = BeautifulSoup(response.text, "lxml")

            for a in soup.find_all("a", href=True):

                href = urljoin(seed, a["href"])

                urls.append(href)

        urls = filter_urls(urls)

        print(f"[DISCOVERY] {len(urls)} ürün URL'si bulundu")

        return urls