from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Candidate:
    """
    Keşif kaynaklarının döndürdüğü ham veri.
    Bu veri henüz doğrulanmış ürün değildir.
    """

    discovery_source: str

    merchant_url: str

    retailer: str

    forum_url: str | None = None

    discovered_title: str | None = None

    discovered_at: str | None = None
