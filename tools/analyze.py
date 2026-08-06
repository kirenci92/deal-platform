"""
Analyzer CLI skeleton for Deal Platform.

This file is a complete command-line entry point that:
- accepts --store and --url
- downloads HTML
- extracts meta, OpenGraph, canonical, JSON-LD and scripts
- writes report.json and report.md

Playwright and network capture are left as extension points if Playwright
is installed in the environment.
"""

import argparse
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def analyze(url: str):
    r = requests.get(url, timeout=30, headers={
        "User-Agent": "Mozilla/5.0"
    })
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    meta = {m.get("name") or m.get("property"): m.get("content")
            for m in soup.find_all("meta")
            if m.get("content")}

    og = {k: v for k, v in meta.items() if k and k.startswith("og:")}

    canonical = None
    c = soup.find("link", rel="canonical")
    if c:
        canonical = c.get("href")

    json_ld = []
    for s in soup.find_all("script", type="application/ld+json"):
        if not s.string:
            continue
        try:
            json_ld.append(json.loads(s.string))
        except Exception:
            pass

    scripts = [x.get("src") for x in soup.find_all("script") if x.get("src")]

    return {
        "url": url,
        "canonical": canonical,
        "meta": meta,
        "opengraph": og,
        "json_ld": json_ld,
        "scripts": scripts,
        "html_file": "page.html",
        "network": [],
    }, r.text


def write_reports(report, html):
    Path("page.html").write_text(html, encoding="utf-8")

    Path("report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    md = [
        "# Analyzer Report",
        "",
        f"URL: {report['url']}",
        "",
        f"Canonical: {report['canonical']}",
        "",
        f"JSON-LD blocks: {len(report['json_ld'])}",
        f"Scripts: {len(report['scripts'])}",
    ]
    Path("report.md").write_text("\n".join(md), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Deal Platform Analyzer")
    parser.add_argument("--store", required=True)
    parser.add_argument("--url", required=True)

    args = parser.parse_args()

    report, html = analyze(args.url)
    report["store"] = args.store
    write_reports(report, html)

    print("Done.")
    print("Generated:")
    print(" - page.html")
    print(" - report.json")
    print(" - report.md")


if __name__ == "__main__":
    main()