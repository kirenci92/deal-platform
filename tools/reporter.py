from __future__ import annotations

from pathlib import Path


class ReportBuilder:
    def __init__(self):
        self.lines: list[str] = []

    def add(self, title: str, value) -> None:
        self.lines.append(f"## {title}")

        if value is None:
            value = "-"

        self.lines.append(str(value))
        self.lines.append("")

    def add_list(self, title: str, values: list) -> None:
        self.lines.append(f"## {title}")

        if not values:
            self.lines.append("-")
        else:
            for item in values:
                self.lines.append(f"- {item}")

        self.lines.append("")

    def add_jsonld_summary(self, jsonld: list[dict]) -> None:
        self.lines.append("## JSON-LD")

        if not jsonld:
            self.lines.append("-")
            self.lines.append("")
            return

        for index, item in enumerate(jsonld, start=1):

            item_type = item.get("@type", "Unknown")

            self.lines.append(
                f"- #{index}: {item_type}"
            )

        self.lines.append("")

    def build(self) -> str:
        return "\n".join(self.lines)

    def save(
        self,
        directory: Path,
    ) -> Path:

        report = directory / "report.md"

        report.write_text(
            self.build(),
            encoding="utf-8",
        )

        return report