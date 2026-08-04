from __future__ import annotations

import json
import re

from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")

    def title(self) -> str | None:
        if self.soup.title:
            return self.soup.title.get_text(strip=True)

        return None

    def canonical(self) -> str | None:
        tag = self.soup.find("link", rel="canonical")

        if tag:
            return tag.get("href")

        return None

    def meta(self, name: str) -> str | None:

        tag = self.soup.find(
            "meta",
            attrs={"name": name},
        )

        if tag:
            return tag.get("content")

        tag = self.soup.find(
            "meta",
            attrs={"property": name},
        )

        if tag:
            return tag.get("content")

        return None

    def json_ld(self) -> list[dict]:

        data = []

        scripts = self.soup.find_all(
            "script",
            attrs={"type": "application/ld+json"},
        )

        for script in scripts:

            if not script.string:
                continue

            try:
                obj = json.loads(script.string)

                if isinstance(obj, list):
                    data.extend(obj)
                else:
                    data.append(obj)

            except Exception:
                pass

        return data

    def all_scripts(self) -> list[str]:

        result = []

        scripts = self.soup.find_all("script")

        for script in scripts:

            if script.string:

                text = script.string.strip()

                if text:
                    result.append(text)

        return result

    def first_price(self) -> str | None:

        patterns = [
            r'"price"\s*:\s*"([^"]+)"',
            r'"price"\s*:\s*([0-9.,]+)',
            r'"salePrice"\s*:\s*"([^"]+)"',
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                self.html,
                flags=re.IGNORECASE,
            )

            if match:
                return match.group(1)

        return None