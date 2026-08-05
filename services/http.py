from __future__ import annotations

import random
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:

    USER_AGENTS = [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0 Safari/537.36"
        ),
    ]

    session = requests.Session()

    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    @classmethod
    def headers(cls) -> dict:

        return {
            "User-Agent": random.choice(cls.USER_AGENTS),
            "Accept": (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Connection": "keep-alive",
        }

    @classmethod
    def get(cls, url: str) -> requests.Response:

        time.sleep(random.uniform(0.5, 1.5))

        response = cls.session.get(
            url,
            headers=cls.headers(),
            timeout=20,
            allow_redirects=True,
        )

        response.raise_for_status()

        return response