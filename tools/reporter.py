import json
import re
from pathlib import Path


def _safe_name(url: str) -> str:
    value = re.sub(r"^https?://", "", url)
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value)
    return value.strip("_")[:120]


def save_report(report):

    report_id = _safe_name(report.url)

    output = (
        Path("analysis")
        / report.store
        / report_id
    )

    output.mkdir(parents=True, exist_ok=True)

    if getattr(report, "html", None):
        (output / "page.html").write_text(
            report.html,
            encoding="utf-8"
        )

    if getattr(report, "rendered_html", None):
        (output / "rendered.html").write_text(
            report.rendered_html,
            encoding="utf-8"
        )

    with open(output / "headers.json", "w", encoding="utf-8") as f:
        json.dump(report.headers, f, indent=2, ensure_ascii=False)

    with open(output / "meta.json", "w", encoding="utf-8") as f:
        json.dump(report.meta, f, indent=2, ensure_ascii=False)

    with open(output / "jsonld.json", "w", encoding="utf-8") as f:
        json.dump(report.json_ld, f, indent=2, ensure_ascii=False)

    with open(output / "scripts.json", "w", encoding="utf-8") as f:
        json.dump(report.scripts, f, indent=2, ensure_ascii=False)

    with open(output / "report.json", "w", encoding="utf-8") as f:
        json.dump(
            report.to_dict(),
            f,
            indent=2,
            ensure_ascii=False
        )