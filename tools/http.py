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


def analyze_http(report):

    response = requests.get(
        report.url,
        headers=DEFAULT_HEADERS,
        timeout=30,
        allow_redirects=True,
    )

    response.raise_for_status()

    report.status_code = response.status_code

    report.final_url = response.url

    report.headers = dict(response.headers)

    report.cookies = {
        cookie.name: cookie.value
        for cookie in response.cookies
    }

    report.html = response.text

    soup = BeautifulSoup(response.text, "lxml")

    report.meta = {}

    for meta in soup.find_all("meta"):

        key = (
            meta.get("name")
            or meta.get("property")
            or meta.get("http-equiv")
        )

        value = meta.get("content")

        if key and value:
            report.meta[key] = value

    report.title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else None
    )

    return report