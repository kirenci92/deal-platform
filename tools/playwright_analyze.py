from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class PlaywrightAnalyzer:

    def __init__(self, url: str):

        self.url = url

        self.output = (
            Path("analysis")
            / urlparse(url).netloc.replace("www.", "").replace(".", "_")
            / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )

        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
            )

            page = browser.new_page()

            page.goto(
                self.url,
                wait_until="networkidle",
                timeout=60000,
            )

            html = page.content()

            (self.output / "page.html").write_text(
                html,
                encoding="utf-8",
            )

            page.screenshot(
                path=str(self.output / "page.png"),
                full_page=True,
            )

            soup = BeautifulSoup(
                html,
                "lxml",
            )

            meta = {
                "title": page.title(),
                "url": page.url,
            }

            canonical = soup.find(
                "link",
                rel="canonical",
            )

            if canonical:
                meta["canonical"] = canonical.get(
                    "href"
                )

            (self.output / "meta.json").write_text(
                json.dumps(
                    meta,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            jsonld_dir = self.output / "jsonld"

            jsonld_dir.mkdir(
                exist_ok=True,
            )

            count = 0

            for script in soup.find_all(
                "script",
                attrs={
                    "type": "application/ld+json",
                },
            ):

                if not script.string:
                    continue

                try:

                    data = json.loads(
                        script.string,
                    )

                except Exception:
                    continue

                count += 1

                (
                    jsonld_dir
                    / f"{count}.json"
                ).write_text(
                    json.dumps(
                        data,
                        indent=4,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

            browser.close()

        print("Playwright analysis completed.")
        print(self.output)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("url")

    args = parser.parse_args()

    PlaywrightAnalyzer(
        args.url,
    ).run()


if __name__ == "__main__":
    main()
