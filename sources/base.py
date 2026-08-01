from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Deal:

    url: str

    store: str

    price: float

    old_price: Optional[float] = None

    discount: Optional[int] = None

    coupon: Optional[str] = None

    image: Optional[str] = None

    stock_status: bool = True

    stock_count: Optional[int] = None

    fingerprint: Optional[str] = None

    source: Optional[str] = None

    category: Optional[str] = None

    brand: Optional[str] = None


class BaseSource(ABC):

    name: str = "Unknown"

    @abstractmethod
    def get_deals(self) -> list[Deal]:
        """
        Kaynaktan fırsatları döndürür.
        """
        raise NotImplementedError