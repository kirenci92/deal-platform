import json

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    )
}


# İleride Discovery, Analyzer ve Scraper aynı session'ı kullanacak.
SESSION = requests.Session()
SESSION.headers.update(DEFAULT_HEADERS)


def analyze_http(report):

    response = SESSION.get(
        report.url,
        timeout=30,
        allow_redirects=True,
    )

    response.raise_for_status()

    # Yanlış charset dönen siteler için
    response.encoding = response.apparent_encoding

    report.status_code = response.status_code
    report.final_url = response.url
    report.response_time = response.elapsed.total_seconds()

    report.headers = dict(response.headers)

    report.cookies = {
        cookie.name: cookie.value
        for cookie in response.cookies
    }

    report.html = response.text

    soup = BeautifulSoup(report.html, "lxml")

    # Sayfa başlığı
    report.title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else None
    )

    # Meta etiketleri
    report.meta = {}

    # OpenGraph etiketleri
    report.opengraph = {}

    for meta in soup.find_all("meta"):

        key = (
            meta.get("name")
            or meta.get("property")
            or meta.get("http-equiv")
        )

        value = meta.get("content")

        if not key or not value:
            continue

        if key.lower().startswith("og:"):
            report.opengraph[key] = value
        else:
            report.meta[key] = value

    # Canonical URL
    canonical = soup.find(
        "link",
        rel=lambda value: value and "canonical" in value.lower(),
    )

    report.canonical = (
        canonical.get("href")
        if canonical
        else None
    )

    # JSON-LD verileri
    report.json_ld = []

    for script in soup.find_all(
        "script",
        type="application/ld+json",
    ):

        if not script.string:
            continue

        try:

            report.json_ld.append(
                json.loads(script.string)
            )

        except Exception:

            # Bazı siteler geçersiz JSON döndürüyor.
            continue

    return report