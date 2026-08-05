from services.discovery.hepsiburada import HepsiburadaDiscovery
from services.discovery.queue import DiscoveryQueue


class DiscoveryRunner:

    def __init__(self):

        self.queue = DiscoveryQueue()

        self.discoveries = [
            HepsiburadaDiscovery(),
        ]

    def discover(self):

        for discovery in self.discoveries:

            print(f"\n[{discovery.store.upper()}] Discovery başladı")

            urls = discovery.discover()

            added = self.queue.extend(urls)

            print(f"Yeni URL : {added}")

    def next_url(self):

        return self.queue.pop()

    def has_work(self):

        return not self.queue.empty()

    def run(self):

        self.discover()

        while self.has_work():

            url = self.next_url()

            print(f"Analyzer Queue -> {url}")

            # Sonraki adımda:
            # AnatomyAnalyzer(...).run()


if __name__ == "__main__":

    DiscoveryRunner().run()