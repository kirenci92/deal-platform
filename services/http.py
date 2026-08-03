from __future__ import annotations

import requests


class HttpClient:

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    )

    @classmethod
    def get(cls, url: str) -> requests.Response:

        response = requests.get(
            url,
            headers={
                "User-Agent": cls.USER_AGENT,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response
