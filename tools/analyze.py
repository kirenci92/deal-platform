import argparse

from tools.schema import AnalysisReport
from tools.http import analyze_http
from tools.playwright_analyze import analyze_playwright
from tools.network_parser import analyze_network
from tools.parser import analyze_dom
from tools.diagnostics import analyze_diagnostics
from tools.reporter import save_report


class AnatomyAnalyzer:

    def __init__(self, store: str, url: str):
        self.report = AnalysisReport(
            store=store,
            url=url,
        )

    def run(self):

        print("[1/6] HTTP Analyzer")
        analyze_http(self.report)

        print("[2/6] Playwright Analyzer")
        analyze_playwright(self.report)

        print("[3/6] Network Parser")
        analyze_network(self.report)

        print("[4/6] DOM Parser")
        analyze_dom(self.report)

        print("[5/6] Diagnostics")
        analyze_diagnostics(self.report)

        print("[6/6] Reporter")
        save_report(self.report)

        print("✓ Analysis completed")

        return self.report


def analyze(store: str, url: str):
    analyzer = AnatomyAnalyzer(store, url)
    return analyzer.run()


def main():

    parser = argparse.ArgumentParser(
        description="Deal Platform Site Anatomy Analyzer"
    )

    parser.add_argument(
        "--store",
        required=True,
        help="Store name (hepsiburada, trendyol...)"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Product URL"
    )

    args = parser.parse_args()

    analyze(
        store=args.store,
        url=args.url,
    )


if __name__ == "__main__":
    main()