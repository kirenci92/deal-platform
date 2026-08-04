import random
import time
from typing import Optional

import requests


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0 Safari/537.36",
]


class HttpClient:
    def __init__(
        self,
        timeout: int = 30,
        retries: int = 3,
    ):
        self.timeout = timeout
        self.retries = retries

        self.session = requests.Session()

    def _headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/avif,"
                "image/webp,"
                "*/*;q=0.8"
            ),
            "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "no-cache",
        }

    def get(self, url: str) -> Optional[requests.Response]:

        last_error = None

        for attempt in range(self.retries):

            try:

                response = self.session.get(
                    url,
                    headers=self._headers(),
                    timeout=self.timeout,
                    allow_redirects=True,
                )

                response.raise_for_status()

                return response

            except Exception as e:

                last_error = e

                time.sleep(2)

        print(last_error)

        return None

    def html(self, url: str) -> Optional[str]:

        response = self.get(url)

        if response is None:
            return None

        return response.text