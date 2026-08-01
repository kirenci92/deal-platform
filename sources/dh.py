import requests
from bs4 import BeautifulSoup


URL = "https://forum.donanimhaber.com/sicak-firsatlar--f193"


def get_deals():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        deals = []

        for a in soup.select("a")[:300]:
            title = a.get_text(strip=True)
            href = a.get("href")

            if not title or len(title) < 20:
                continue

            if not href:
                continue

            if href.startswith("/"):
                href = "https://forum.donanimhaber.com" + href

            deals.append(
                {
                    "title": title,
                    "url": href,
                }
            )

            if len(deals) >= 10:
                break

        return deals

    except Exception as e:
        print(e)
        return []
