from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Deal:
    """
    Platformdaki bütün scraper'ların döndürmek zorunda olduğu ortak veri modeli.
    """

    # Gerçek ürün bilgileri
    title: str
    product_url: str
    retailer: str

    # Fiyat
    price: float
    old_price: Optional[float] = None
    discount: Optional[int] = None

    # Kampanya
    coupon: Optional[str] = None

    # Görseller
    image_url: Optional[str] = None

    # Marka / kategori
    brand: Optional[str] = None
    category: Optional[str] = None

    # Satıcı
    seller: Optional[str] = None

    # Stok
    in_stock: bool = True
    stock_count: Optional[int] = None

    # Kimlik
    product_id: Optional[str] = None
    fingerprint: Optional[str] = None

    # İç sistem (Telegram'da gösterilmeyecek)
    discovery_source: Optional[str] = None

    discovered_at: datetime = datetime.utcnow()


class BaseSource(ABC):

    name: str = "Unknown"

    @abstractmethod
    def get_deals(self) -> list[Deal]:
        """
        Kaynaktaki doğrulanmış fırsatları döndürür.
        """
        raise NotImplementedError