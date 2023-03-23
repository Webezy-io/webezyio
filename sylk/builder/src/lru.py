from collections import OrderedDict
from typing import Generic, Hashable, Iterator, Optional, TypeVar

T = TypeVar("T")

class LruCache(Generic[T]):
    def __init__(self, capacity: int, cache: "OrderedDict[Hashable, T]" = OrderedDict()):
        self.capacity = capacity
        self.__cache: OrderedDict[Hashable, T] = cache

    def get(self, key: Hashable) -> Optional[T]:
        if key not in self.__cache:
            return None
        self.__cache.move_to_end(key)

        return self.__cache[key]

    def insert(self, key: Hashable, value: T) -> None:
        if len(self.__cache) == self.capacity:
            self.__cache.popitem(last=False)
        self.__cache[key] = value
        self.__cache.move_to_end(key)

    def __len__(self) -> int:
        return len(self.__cache)

    def clear(self) -> None:
        self.__cache.clear()

    def iterate(self) -> Iterator[Optional[T]]:
        for k in self.__cache:
            yield self.__cache[k]

