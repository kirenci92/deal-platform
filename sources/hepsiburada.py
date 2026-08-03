from __future__ import annotations

from sources.base import BaseSource, Deal
from sources.candidate import Candidate


class Hepsiburada(BaseSource):

    name = "Hepsiburada"

    def extract(self, candidate: Candidate) -> Deal | None:
        raise NotImplementedError

    def get_deals(self) -> list[Deal]:
        return []
