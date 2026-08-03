from __future__ import annotations

from sources.base import Deal
from sources.candidate import Candidate

from sources.amazon import Amazon
from sources.hepsiburada import Hepsiburada
from sources.trendyol import Trendyol


class Resolver:

    def __init__(self):

        self.extractors = {
            "Amazon": Amazon(),
            "Hepsiburada": Hepsiburada(),
            "Trendyol": Trendyol(),
        }

    def resolve(self, candidate: Candidate) -> Deal | None:

        extractor = self.extractors.get(candidate.retailer)

        if extractor is None:
            return None

        return extractor.extract(candidate)
