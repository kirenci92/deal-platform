from playwright.sync_api import sync_playwright


def analyze_playwright(report):

    requests = []
    responses = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/139.0 Safari/537.36"
            )
        )

        def on_request(request):

            requests.append(
                {
                    "method": request.method,
                    "url": request.url,
                    "resource_type": request.resource_type,
                }
            )

        def on_response(response):

            try:
                content_type = response.headers.get(
                    "content-type",
                    "",
                )
            except Exception:
                content_type = ""

            responses.append(
                {
                    "url": response.url,
                    "status": response.status,
                    "content_type": content_type,
                }
            )

        page.on("request", on_request)
        page.on("response", on_response)

        try:

            page.goto(
                report.url,
                wait_until="networkidle",
                timeout=60000,
            )

            report.rendered_html = page.content()

            report.screenshot_path = (
                f"analysis/{report.store}/screenshot.png"
            )

            page.screenshot(
                path=report.screenshot_path,
                full_page=True,
            )

            html = report.rendered_html.lower()

            if "__next" in html:
                report.framework = "Next.js"

            elif "__nuxt" in html:
                report.framework = "Nuxt"

            elif "webpack" in html:
                report.framework = "Webpack"

            else:
                report.framework = "Unknown"

        finally:

            browser.close()

    report.network = {
        "requests": requests,
        "responses": responses,
    }

    return report