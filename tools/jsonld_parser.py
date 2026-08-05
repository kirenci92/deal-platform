from typing import Any, Dict, List


def _as_list(data: Any) -> List[Dict]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        if "@graph" in data and isinstance(data["@graph"], list):
            return [x for x in data["@graph"] if isinstance(x, dict)]
        return [data]
    return []


def analyze_jsonld(report):

    report.product_jsonld = {}

    for document in report.json_ld:

        for node in _as_list(document):

            node_type = node.get("@type", "")

            if isinstance(node_type, list):
                node_type = ",".join(node_type)

            node_type = str(node_type).lower()

            if "product" not in node_type:
                continue

            offers = node.get("offers", {})

            if isinstance(offers, list):
                offers = offers[0] if offers else {}

            report.product_jsonld = {
                "name": node.get("name"),
                "brand": (
                    node.get("brand", {}).get("name")
                    if isinstance(node.get("brand"), dict)
                    else node.get("brand")
                ),
                "sku": node.get("sku"),
                "image": node.get("image"),
                "description": node.get("description"),
                "price": offers.get("price"),
                "currency": offers.get("priceCurrency"),
                "availability": offers.get("availability"),
                "url": node.get("url"),
                "rating": (
                    node.get("aggregateRating", {}).get("ratingValue")
                    if isinstance(node.get("aggregateRating"), dict)
                    else None
                ),
                "review_count": (
                    node.get("aggregateRating", {}).get("reviewCount")
                    if isinstance(node.get("aggregateRating"), dict)
                    else None
                ),
            }

            return report

    return report
