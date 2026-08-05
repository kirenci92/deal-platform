from abc import ABC, abstractmethod
from typing import Iterable


class Discovery(ABC):
    """
    Discovery Engine

    Görevi sadece ürün URL'lerini bulmaktır.
    Hiçbir parse veya analiz yapmaz.
    """

    @property
    @abstractmethod
    def store(self) -> str:
        ...

    @abstractmethod
    def discover(self) -> Iterable[str]:
        """
        Product URL'leri döndürür.
        """
        raise NotImplementedError
