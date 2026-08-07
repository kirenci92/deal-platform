from urllib.parse import urlparse


API_KEYWORDS = (
    "api",
    "graphql",
    "search",
    "product",
    "products",
    "listing",
    "campaign",
    "offer",
    "offers",
    "recommend",
)


def analyze_network(report):

    report.api_endpoints = []

    report.static_assets = []

    report.xhr_requests = []

    seen = set()

    network = getattr(
        report,
        "network",
        {},
    )

    for response in network.get(
        "responses",
        [],
    ):

        url = response.get(
            "url",
            "",
        )

        if not url or url in seen:
            continue

        seen.add(url)

        status = response.get("status")

        content_type = response.get(
            "content_type",
            "",
        ).lower()

        parsed = urlparse(url)

        path = parsed.path.lower()

        endpoint = {
            "url": url,
            "path": path,
            "status": status,
            "content_type": content_type,
        }

        if (
            "application/json" in content_type
            or any(
                keyword in path
                for keyword in API_KEYWORDS
            )
        ):

            report.api_endpoints.append(
                endpoint
            )

        if any(
            ext in path
            for ext in (
                ".js",
                ".css",
                ".png",
                ".jpg",
                ".jpeg",
                ".svg",
                ".webp",
            )
        ):

            report.static_assets.append(
                endpoint
            )

        if (
            "json" in content_type
            or "graphql" in path
        ):

            report.xhr_requests.append(
                endpoint
            )

    report.api_endpoints.sort(
        key=lambda item: item["url"]
    )

    report.static_assets.sort(
        key=lambda item: item["url"]
    )

    report.xhr_requests.sort(
        key=lambda item: item["url"]
    )

    return report