from __future__ import annotations

from abc import ABC

from sources.base import BaseSource, Deal
from sources.candidate import Candidate


class Amazon(BaseSource):

    name = "Amazon"

    def extract(self, candidate: Candidate) -> Deal | None:
        """
        Candidate içindeki Amazon linkinden
        gerçek ürün bilgilerini üretir.
        """

        # Şimdilik iskelet.
        # requests + BeautifulSoup burada kullanılacak.

        raise NotImplementedError

    def get_deals(self) -> list[Deal]:
        """
        Discovery katmanı kullanılacağı için
        doğrudan çağrılmayacak.
        """
        return []
