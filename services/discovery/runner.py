from typing import Dict, List

from services.discovery.hepsiburada import HepsiburadaDiscovery


class DiscoveryRunner:

    def __init__(self):

        self.discoveries = [
            HepsiburadaDiscovery(),
        ]

    def run(self) -> Dict[str, List[str]]:

        result = {}

        for discovery in self.discoveries:

            print(f"[DISCOVERY] {discovery.store}")

            urls = list(discovery.discover())

            urls = sorted(set(urls))

            result[discovery.store] = urls

            print(f"  {len(urls)} URL bulundu")

        return result


if __name__ == "__main__":

    runner = DiscoveryRunner()

    data = runner.run()

    total = sum(len(v) for v in data.values())

    print(f"\nToplam {total} ürün URL'si bulundu.")
