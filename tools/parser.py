import json
from bs4 import BeautifulSoup


def analyze_dom(report):

    html = getattr(report, "rendered_html", None) or getattr(report, "html", "")

    soup = BeautifulSoup(html, "lxml")

    # Title
    if soup.title and soup.title.string:
        report.title = soup.title.string.strip()

    # Canonical
    canonical = soup.find("link", rel="canonical")
    report.canonical = canonical.get("href") if canonical else None

    # OpenGraph
    report.opengraph = {}

    for meta in soup.find_all("meta", property=True):
        prop = meta.get("property")
        if prop.startswith("og:"):
            report.opengraph[prop] = meta.get("content")

    # JSON-LD
    report.json_ld = []

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            report.json_ld.append(json.loads(tag.string))
        except Exception:
            continue

    # Script kaynakları
    report.scripts = []

    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            report.scripts.append(src)

    return report