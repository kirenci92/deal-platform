from services.discovery.hepsiburada import HepsiburadaDiscovery
from services.discovery.queue import DiscoveryQueue
from tools.analyze import AnatomyAnalyzer


class DiscoveryRunner:

    def __init__(self):

        self.queue = DiscoveryQueue()

        self.discoveries = [
            HepsiburadaDiscovery(),
        ]

    def discover(self):

        for discovery in self.discoveries:

            print(f"\n[{discovery.store.upper()}] Discovery")

            urls = discovery.discover()

            added = self.queue.extend(urls)

            print(f"Yeni URL : {added}")

    def process(self):

        while not self.queue.empty():

            url = self.queue.pop()

            print(f"\n[ANALYZER] {url}")

            AnatomyAnalyzer(
                store="hepsiburada",
                url=url,
            ).run()

    def run(self):

        self.discover()

        self.process()


if __name__ == "__main__":

    DiscoveryRunner().run()