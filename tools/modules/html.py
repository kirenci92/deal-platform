from __future__ import annotations

from pathlib import Path

from services.http import HttpClient


class HtmlDownloader:
    """
    Bir URL'yi indirir ve HTML içeriğini döndürür.
    """

    @staticmethod
    def download(url: str) -> str:

        response = HttpClient.get(url)

        return response.text

    @staticmethod
    def save(directory: Path, html: str) -> Path:

        file = directory / "page.html"

        file.write_text(
            html,
            encoding="utf-8",
        )

        return file