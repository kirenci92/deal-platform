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

    seen = set()

    network = getattr(report, "network", {})

    for response in network.get("responses", []):

        url = response.get("url", "")

        content_type = response.get("content_type", "").lower()

        parsed = urlparse(url)

        path = parsed.path.lower()

        if (
            "application/json" in content_type
            or any(keyword in path for keyword in API_KEYWORDS)
        ):

            if url not in seen:

                seen.add(url)

                report.api_endpoints.append({
                    "url": url,
                    "path": path,
                    "status": response.get("status"),
                    "content_type": content_type,
                })

    return report
