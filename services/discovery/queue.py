from collections import deque
from typing import Iterable, Optional


class DiscoveryQueue:

    def __init__(self):
        self._queue = deque()
        self._seen = set()

    def add(self, url: str) -> bool:
        """
        Yeni URL ise kuyruğa ekler.
        Aynı URL tekrar eklenmez.
        """
        if url in self._seen:
            return False

        self._seen.add(url)
        self._queue.append(url)
        return True

    def extend(self, urls: Iterable[str]) -> int:
        """
        Toplu URL ekler.
        Eklenen yeni URL sayısını döndürür.
        """
        count = 0

        for url in urls:
            if self.add(url):
                count += 1

        return count

    def pop(self) -> Optional[str]:
        """
        Kuyruktan sıradaki URL'yi alır.
        """
        if not self._queue:
            return None

        return self._queue.popleft()

    def empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)

    def clear(self):
        self._queue.clear()
        self._seen.clear()
