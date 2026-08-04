from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class FileSystem:
    def __init__(self, base_dir: str = "analysis"):
        self.base_dir = Path(base_dir)

    def create_session(self, source: str) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        session_dir = self.base_dir / source / timestamp
        session_dir.mkdir(parents=True, exist_ok=True)

        return session_dir

    def save_html(self, directory: Path, html: str) -> Path:
        path = directory / "page.html"

        path.write_text(
            html,
            encoding="utf-8",
        )

        return path

    def save_json(
        self,
        directory: Path,
        filename: str,
        data: dict,
    ) -> Path:

        path = directory / filename

        path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path

    def save_text(
        self,
        directory: Path,
        filename: str,
        text: str,
    ) -> Path:

        path = directory / filename

        path.write_text(
            text,
            encoding="utf-8",
        )

        return path