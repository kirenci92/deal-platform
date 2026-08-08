from __future__ import annotations

import time
import requests

from tools.schema import AnalysisReport


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


def analyze_http(report: AnalysisReport):

    start = time.perf_counter()

    try:
        response = HttpClient.get(report.url)

        report.status_code = response.status_code
        report.final_url = response.url
        report.response_time = time.perf_counter() - start

        report.headers = dict(response.headers)
        report.cookies = response.cookies.get_dict()
        report.html = response.text

    except requests.RequestException as exc:

        report.response_time = time.perf_counter() - start

        if exc.response is not None:
            report.status_code = exc.response.status_code
            report.final_url = exc.response.url
            report.headers = dict(exc.response.headers)
            report.cookies = exc.response.cookies.get_dict()
            report.html = exc.response.text

        report.notes.append(f"HTTP error: {exc}")

    except Exception as exc:

        report.notes.append(f"HTTP unexpected error: {exc}")

    return report