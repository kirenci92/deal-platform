import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


PRICE_RE = re.compile(
    r"(\d[\d\.\,]*)\s*(₺|TL|TRY)",
    re.IGNORECASE,
)


def _text(node):

    if not node:
        return ""

    return " ".join(
        node.get_text(
            " ",
            strip=True,
        ).split()
    )


def _score(node):

    score = 0

    text = _text(node)
    html = str(node).lower()

    if PRICE_RE.search(text):
        score += 30

    if node.find("img"):
        score += 20

    if node.find("a", href=True):
        score += 20

    if "product" in html:
        score += 15

    if "price" in html:
        score += 15

    return score


def _selector(node):

    if node.get("id"):
        return f"#{node.get('id')}"

    classes = node.get("class", [])

    if classes:
        return (
            node.name
            + "."
            + ".".join(classes[:3])
        )

    return node.name


def analyze_dom(report):

    html = (
        getattr(report, "rendered_html", None)
        or getattr(report, "html", "")
    )

    soup = BeautifulSoup(
        html,
        "lxml",
    )

    candidates = []

    for node in soup.find_all(
        [
            "article",
            "div",
            "li",
        ]
    ):

        score = _score(node)

        if score >= 40:
            candidates.append(
                (
                    score,
                    node,
                )
            )

    candidates.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    report.selector_candidates = []

    if not candidates:
        return report

    best = candidates[0][1]

    report.selector_candidates = [
        {
            "tag": node.name,
            "id": node.get("id"),
            "class": node.get(
                "class",
                [],
            ),
            "selector": _selector(node),
            "score": score,
        }
        for score, node in candidates[:20]
    ]

    title = ""

    for tag in best.find_all(
        [
            "h1",
            "h2",
            "h3",
            "span",
            "a",
        ]
    ):

        value = _text(tag)

        if len(value) > len(title):
            title = value

    image = best.find("img")

    image_url = None

    if image:

        image_url = (
            image.get("src")
            or image.get("data-src")
            or image.get("data-original")
        )

    if image_url:
        image_url = urljoin(
            report.final_url or report.url,
            image_url,
        )

    link = best.find(
        "a",
        href=True,
    )

    product_url = None

    if link:

        product_url = urljoin(
            report.final_url or report.url,
            link["href"],
        )

    prices = PRICE_RE.findall(
        _text(best)
    )

    report.product_candidate = {
        "title": title,
        "price": (
            prices[0][0]
            if prices
            else None
        ),
        "image": image_url,
        "link": product_url,
    }

    return report