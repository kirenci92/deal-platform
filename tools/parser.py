import re
from bs4 import BeautifulSoup


PRICE_PATTERN = re.compile(r"(₺|TL|TRY|\d+[.,]\d{2})", re.IGNORECASE)


def _text(tag):
    if not tag:
        return ""

    return " ".join(tag.get_text(" ", strip=True).split())


def _score(node):

    score = 0

    text = _text(node)

    html = str(node).lower()

    if PRICE_PATTERN.search(text):
        score += 30

    if node.find("img"):
        score += 20

    if node.find("a", href=True):
        score += 20

    if len(node.find_all()) >= 5:
        score += 10

    if "product" in html:
        score += 10

    if "price" in html:
        score += 10

    return score


def analyze_dom(report):

    html = getattr(report, "rendered_html", None)

    if not html:
        html = getattr(report, "html", "")

    soup = BeautifulSoup(html, "lxml")

    report.selector_candidates = []

    candidates = soup.find_all(["article", "li", "div"])

    scored = []

    for node in candidates:

        score = _score(node)

        if score < 40:
            continue

        scored.append((score, node))

    scored.sort(key=lambda x: x[0], reverse=True)

    for score, node in scored[:20]:

        report.selector_candidates.append(
            {
                "tag": node.name,
                "class": node.get("class", []),
                "id": node.get("id"),
                "score": score,
            }
        )

    return report