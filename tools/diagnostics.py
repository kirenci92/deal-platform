from __future__ import annotations

import json
import sys
from urllib.parse import urlparse

from filesystem import FileSystem
from http import HttpClient
from parser import PageParser
from reporter import ReportBuilder


def detect_source(url: str) -> str:
    host = urlparse(url).netloc.lower()

    host = host.replace("www.", "")

    return host.replace(".", "_")


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python tools/diagnostics.py <URL>")
        return

    url = sys.argv[1]

    source = detect_source(url)

    fs = FileSystem()

    session = fs.create_session(source)

    client = HttpClient()

    response = client.get(url)

    if response is None:
        print("Request failed.")
        return

    html = response.text

    fs.save_html(session, html)

    fs.save_json(
        session,
        "headers.json",
        dict(response.headers),
    )

    parser = PageParser(html)

    jsonld = parser.json_ld()

    for index, item in enumerate(jsonld, start=1):

        fs.save_json(
            session,
            f"jsonld_{index}.json",
            item,
        )

    meta = {
        "url": response.url,
        "status": response.status_code,
        "title": parser.title(),
        "canonical": parser.canonical(),
        "description": parser.meta("description"),
        "og:title": parser.meta("og:title"),
        "og:image": parser.meta("og:image"),
        "og:type": parser.meta("og:type"),
        "price": parser.first_price(),
    }

    fs.save_json(
        session,
        "meta.json",
        meta,
    )

    report = ReportBuilder()

    report.add("URL", meta["url"])

    report.add("STATUS", meta["status"])

    report.add("TITLE", meta["title"])

    report.add("CANONICAL", meta["canonical"])

    report.add("DESCRIPTION", meta["description"])

    report.add("OG TITLE", meta["og:title"])

    report.add("OG IMAGE", meta["og:image"])

    report.add("PRICE", meta["price"])

    report.add(
        "JSON-LD COUNT",
        len(jsonld),
    )

    report.add_jsonld_summary(jsonld)

    report.save(session)

    print()

    print("Diagnostics completed.")

    print(session)


if __name__ == "__main__":
    main()