from typing import List
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from services.discovery.url_filter import filter_urls


class PlaywrightDiscovery:

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def discover(self, url: str) -> List[str]:

        urls = []

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                user_agent=self.user_agent
            )

            page = context.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000,
            )

            # Lazy Loading
            previous_height = 0

            for _ in range(10):

                page.evaluate(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )

                page.wait_for_timeout(1000)

                height = page.evaluate(
                    "document.body.scrollHeight"
                )

                if height == previous_height:
                    break

                previous_height = height

            for href in page.eval_on_selector_all(
                "a[href]",
                "els => els.map(e => e.href)"
            ):
                urls.append(urljoin(url, href))

            browser.close()

        return filter_urls(urls)
