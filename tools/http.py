import argparse

from tools.schema import AnalysisReport
from tools.http_client import analyze_http
from tools.playwright_analyze import analyze_playwright
from tools.network_parser import analyze_network
from tools.parser import analyze_dom
from tools.jsonld_parser import analyze_jsonld
from tools.diagnostics import analyze_diagnostics
from tools.reporter import save_report


class AnatomyAnalyzer:

    def __init__(self, store: str, url: str):
        self.report = AnalysisReport(
            store=store,
            url=url,
        )

    def run(self):

        print("[1/7] HTTP")
        analyze_http(self.report)

        print("[2/7] Playwright")
        analyze_playwright(self.report)

        print("[3/7] Network")
        analyze_network(self.report)

        print("[4/7] DOM")
        analyze_dom(self.report)

        print("[5/7] JSON-LD")
        analyze_jsonld(self.report)

        print("[6/7] Diagnostics")
        analyze_diagnostics(self.report)

        print("[7/7] Reporter")
        save_report(self.report)

        print("✓ Done")

        return self.report


def analyze(store: str, url: str):
    return AnatomyAnalyzer(store, url).run()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--store", required=True)
    parser.add_argument("--url", required=True)

    args = parser.parse_args()

    analyze(args.store, args.url)


if __name__ == "__main__":
    main()