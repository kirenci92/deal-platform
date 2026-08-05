from datetime import datetime
from pathlib import Path
import hashlib


class AnalysisWorkspace:

    def __init__(self, root="analysis"):
        self.root = Path(root)

    def create(self, store: str, url: str):

        url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        directory = (
            self.root
            / store
            / f"{timestamp}_{url_hash}"
        )

        directory.mkdir(parents=True, exist_ok=True)

        return {
            "root": directory,
            "report": directory / "report.json",
            "html": directory / "page.html",
            "rendered_html": directory / "rendered.html",
            "headers": directory / "headers.json",
            "meta": directory / "meta.json",
            "jsonld": directory / "jsonld.json",
            "scripts": directory / "scripts.json",
            "network": directory / "network.json",
            "screenshot": directory / "screenshot.png",
        }