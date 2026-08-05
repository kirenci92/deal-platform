import re
from urllib.parse import urlparse


PRODUCT_PATTERNS = [
    re.compile(r"/.+-p-[A-Za-z0-9]+/?$", re.IGNORECASE),
]


EXCLUDED_PATHS = (
    "/giris",
    "/uye",
    "/hesabim",
    "/yardim",
    "/iletisim",
    "/destek",
    "/sepet",
    "/odeme",
    "/siparis",
    "/arama",
    "/search",
    "/login",
    "/logout",
)


EXCLUDED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".css",
    ".js",
    ".pdf",
    ".zip",
)


def normalize(url: str) -> str:

    url = url.split("#")[0]
    url = url.split("?")[0]

    if url.endswith("/"):
        url = url[:-1]

    return url


def is_product_url(url: str) -> bool:

    path = urlparse(url).path

    return any(pattern.search(path) for pattern in PRODUCT_PATTERNS)


def should_skip(url: str) -> bool:

    path = urlparse(url).path.lower()

    if path.endswith(EXCLUDED_EXTENSIONS):
        return True

    return any(path.startswith(prefix) for prefix in EXCLUDED_PATHS)


def filter_urls(urls):

    result = []

    seen = set()

    for url in urls:

        url = normalize(url)

        if url in seen:
            continue

        if should_skip(url):
            continue

        if not is_product_url(url):
            continue

        seen.add(url)

        result.append(url)

    return result