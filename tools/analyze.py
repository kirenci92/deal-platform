from pathlib import Path

from tools.schema import AnalysisReport
from tools.http import analyze_http
from tools.playwright_analyze import analyze_playwright
from tools.parser import analyze_dom
from tools.diagnostics import analyze_diagnostics
from tools.reporter import save_report


class AnatomyAnalyzer:

    def __init__(self, store: str, url: str):
        self.report = AnalysisReport(
            store=store,
            url=url
        )

    def run(self):

        analyze_http(self.report)

        analyze_playwright(self.report)

        analyze_dom(self.report)

        analyze_diagnostics(self.report)

        save_report(self.report)

        return self.report


def analyze(store: str, url: str):
    analyzer = AnatomyAnalyzer(store, url)
    return analyzer.run()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--store", required=True)
    parser.add_argument("--url", required=True)

    args = parser.parse_args()

    analyze(args.store, args.url)