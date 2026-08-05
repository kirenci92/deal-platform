from pathlib import Path
from playwright.sync_api import sync_playwright


def analyze_playwright(report):

    output_dir = (
        Path("analysis")
        / report.store
        / "temp"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = output_dir / "screenshot.png"
    html_path = output_dir / "page.html"

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            report.url,
            wait_until="networkidle",
            timeout=60000
        )

        page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        html = page.content()

        html_path.write_text(
            html,
            encoding="utf-8"
        )

        report.rendered_html = html

        report.html_path = str(html_path)

        report.screenshot_path = str(screenshot_path)

        browser.close()

    return report