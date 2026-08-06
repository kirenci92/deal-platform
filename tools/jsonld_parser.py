from typing import Any, Dict, List


def _as_list(data: Any) -> List[Dict]:
    """
    JSON-LD farklı formatlarda gelebilir:

    - {}
    - []
    - {"@graph": [...]}

    Hepsini ortak liste formatına dönüştürür.
    """

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if isinstance(data, dict):

        graph = data.get("@graph")

        if isinstance(graph, list):
            return [item for item in graph if isinstance(item, dict)]

        return [data]

    return []


def analyze_jsonld(report):

    report.product_jsonld = {}

    if not getattr(report, "json_ld", None):
        return report

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

            aggregate = node.get("aggregateRating", {})

            if not isinstance(aggregate, dict):
                aggregate = {}

            brand = node.get("brand")

            if isinstance(brand, dict):
                brand = brand.get("name")

            report.product_jsonld = {
                "name": node.get("name"),
                "brand": brand,
                "sku": node.get("sku"),
                "gtin": node.get("gtin"),
                "mpn": node.get("mpn"),
                "description": node.get("description"),
                "image": node.get("image"),
                "url": node.get("url"),
                "price": offers.get("price"),
                "currency": offers.get("priceCurrency"),
                "availability": offers.get("availability"),
                "seller": (
                    offers.get("seller", {}).get("name")
                    if isinstance(offers.get("seller"), dict)
                    else None
                ),
                "rating": aggregate.get("ratingValue"),
                "review_count": aggregate.get("reviewCount"),
            }

            return report

    return report