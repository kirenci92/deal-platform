from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from services.http import HttpClient


class SiteAnalyzer:

    def __init__(self, url: str):

        self.url = url

        self.response = HttpClient.get(url)

        self.html = self.response.text

        self.soup = BeautifulSoup(
            self.html,
            "lxml",
        )

        self.host = (
            urlparse(self.response.url)
            .netloc
            .replace("www.", "")
            .replace(".", "_")
        )

        self.output = (
            Path("analysis")
            / self.host
            / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )

        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_html(self):

        (self.output / "page.html").write_text(
            self.html,
            encoding="utf-8",
        )

    def save_headers(self):

        (self.output / "headers.json").write_text(
            json.dumps(
                dict(self.response.headers),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def save_meta(self):

        meta = {
            "url": self.response.url,
            "status": self.response.status_code,
            "title": (
                self.soup.title.text.strip()
                if self.soup.title
                else None
            ),
        }

        canonical = self.soup.find(
            "link",
            rel="canonical",
        )

        if canonical:

            meta["canonical"] = canonical.get(
                "href"
            )

        description = self.soup.find(
            "meta",
            attrs={
                "name": "description",
            },
        )

        if description:

            meta["description"] = (
                description.get("content")
            )

        (self.output / "meta.json").write_text(
            json.dumps(
                meta,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def save_jsonld(self):

        directory = self.output / "jsonld"

        directory.mkdir(exist_ok=True)

        count = 0

        for script in self.soup.find_all(
            "script",
            attrs={
                "type": "application/ld+json",
            },
        ):

            if not script.string:
                continue

            try:

                data = json.loads(script.string)

            except Exception:
                continue

            count += 1

            (
                directory
                / f"{count}.json"
            ).write_text(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        return count

    def save_scripts(self):

        directory = self.output / "scripts"

        directory.mkdir(exist_ok=True)

        count = 0

        for script in self.soup.find_all(
            "script",
        ):

            text = script.string

            if not text:
                continue

            text = text.strip()

            if not text:
                continue

            count += 1

            (
                directory
                / f"{count}.js"
            ).write_text(
                text,
                encoding="utf-8",
            )

        return count

    def report(
        self,
        jsonld_count: int,
        script_count: int,
    ):

        report = f"""
URL:
{self.response.url}

STATUS:
{self.response.status_code}

TITLE:
{self.soup.title.text.strip() if self.soup.title else "-"}

HTML SIZE:
{len(self.html):,} bytes

JSON-LD:
{jsonld_count}

SCRIPTS:
{script_count}
"""

        (
            self.output
            / "report.md"
        ).write_text(
            report.strip(),
            encoding="utf-8",
        )

    def run(self):

        self.save_html()

        self.save_headers()

        self.save_meta()

        jsonld = self.save_jsonld()

        scripts = self.save_scripts()

        self.report(
            jsonld,
            scripts,
        )

        print()

        print("Analysis completed")

        print(self.output)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
    )

    args = parser.parse_args()

    SiteAnalyzer(
        args.url,
    ).run()


if __name__ == "__main__":
    main()
