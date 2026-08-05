import re
from bs4 import BeautifulSoup


PRICE_RE = re.compile(r"(\d[\d\.\,]*)\s*(₺|TL|TRY)", re.IGNORECASE)


def _text(node):
    if not node:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


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


def analyze_dom(report):

    html = getattr(report, "rendered_html", None) or getattr(report, "html", "")

    soup = BeautifulSoup(html, "lxml")

    candidates = []

    for node in soup.find_all(["article", "div", "li"]):

        score = _score(node)

        if score >= 40:
            candidates.append((score, node))

    candidates.sort(key=lambda x: x[0], reverse=True)

    report.selector_candidates = []

    if not candidates:
        return report

    best = candidates[0][1]

    report.selector_candidates = [
        {
            "tag": n.name,
            "class": n.get("class", []),
            "id": n.get("id"),
            "score": s,
        }
        for s, n in candidates[:20]
    ]

    title = ""

    for tag in best.find_all(["h1", "h2", "h3", "span", "a"]):

        value = _text(tag)

        if len(value) > len(title):
            title = value

    image = best.find("img")

    link = best.find("a", href=True)

    prices = PRICE_RE.findall(_text(best))

    report.product_candidate = {
        "title": title,
        "price": prices[0][0] if prices else None,
        "image": image.get("src") if image else None,
        "link": link.get("href") if link else None,
    }

    return report