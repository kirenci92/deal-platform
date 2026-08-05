from typing import Dict, List


class SeedManager:

    _SEEDS: Dict[str, List[str]] = {

        "hepsiburada": [
            "https://www.hepsiburada.com/",
            "https://www.hepsiburada.com/kampanyalar",
            "https://www.hepsiburada.com/cok-satanlar",
            "https://www.hepsiburada.com/yeni-gelen-urunler",
        ],

        "trendyol": [

        ],

        "amazon": [

        ],

        "n11": [

        ],
    }

    @classmethod
    def get(cls, store: str) -> List[str]:

        return cls._SEEDS.get(
            store.lower(),
            []
        ).copy()

    @classmethod
    def add(cls, store: str, url: str):

        store = store.lower()

        cls._SEEDS.setdefault(
            store,
            []
        )

        if url not in cls._SEEDS[store]:
            cls._SEEDS[store].append(url)

    @classmethod
    def remove(cls, store: str, url: str):

        store = store.lower()

        if store not in cls._SEEDS:
            return

        if url in cls._SEEDS[store]:
            cls._SEEDS[store].remove(url)

    @classmethod
    def all(cls):

        return cls._SEEDS.copy()
