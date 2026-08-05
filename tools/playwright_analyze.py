from playwright.sync_api import sync_playwright


def analyze_playwright(report):

    requests = []
    responses = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        def on_request(request):
            requests.append({
                "method": request.method,
                "url": request.url,
                "resource_type": request.resource_type,
            })

        def on_response(response):
            try:
                content_type = response.headers.get("content-type", "")
            except Exception:
                content_type = ""

            responses.append({
                "url": response.url,
                "status": response.status,
                "content_type": content_type,
            })

        page.on("request", on_request)
        page.on("response", on_response)

        page.goto(
            report.url,
            wait_until="networkidle",
            timeout=60000,
        )

        report.rendered_html = page.content()

        browser.close()

    report.network = {
        "requests": requests,
        "responses": responses,
    }

    return report