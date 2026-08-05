import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from services.discovery.base import Discovery
from services.discovery.seed_manager import SeedManager
from services.discovery.url_filter import filter_urls
from services.discovery.playwright_discovery import PlaywrightDiscovery


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/139.0.0.0 Safari/537.36"
)


class HepsiburadaDiscovery(Discovery):

    @property
    def store(self):
        return "hepsiburada"

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": USER_AGENT,
        })

        self.playwright = PlaywrightDiscovery(
            user_agent=USER_AGENT
        )

    def _requests_discover(self, url):

        links = []

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        for a in soup.find_all("a", href=True):

            href = urljoin(
                url,
                a["href"]
            )

            links.append(href)

        return filter_urls(links)

    def discover(self):

        discovered = set()

        for seed in SeedManager.get(self.store):

            print(f"[DISCOVERY] {seed}")

            try:

                urls = self._requests_discover(seed)

            except Exception as exc:

                print(exc)

                urls = []

            # Requests yeterliyse Playwright çalıştırma
            if len(urls) < 20:

                print("[DISCOVERY] Playwright fallback")

                try:

                    urls.extend(
                        self.playwright.discover(seed)
                    )

                except Exception as exc:

                    print(exc)

            discovered.update(
                filter_urls(urls)
            )

        return sorted(discovered)