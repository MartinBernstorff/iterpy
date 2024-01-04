import multiprocessing
from collections import defaultdict
from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Sequence,
)
from copy import deepcopy
from functools import reduce
from itertools import islice
from typing import Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class Iter(Generic[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        self.__consumable_iterator: Iterator[T] = iter(iterable)

    @property
    def _iterator(self) -> Iterator[T]:
        if isinstance(self.__consumable_iterator, Generator):
            collected = list(self.__consumable_iterator)
            return iter(collected)

        return deepcopy(self.__consumable_iterator)

    def __getitem__(self, index: int | slice) -> T | "Iter[T]":
        if isinstance(index, int) and index >= 0:
            try:
                return list(self._iterator)[index]
            except StopIteration:
                raise IndexError("Index out of range") from None
        elif isinstance(index, slice):
            return Iter(
                islice(
                    self._iterator,
                    index.start,
                    index.stop,
                    index.step,
                )
            )
        else:
            raise KeyError(
                f"Key must be non-negative integer or slice, not {index}"
            )

    ### Reductions
    def reduce(self, func: Callable[[T, T], T]) -> T:
        return reduce(func, self._iterator)

    def count(self) -> int:
        return sum(1 for _ in self._iterator)

    ### Output
    def to_list(self) -> list[T]:
        return list(self._iterator)

    def to_tuple(self) -> tuple[T, ...]:
        return tuple(self._iterator)  # pragma: no cover

    def to_consumable(self) -> Iterator[T]:
        return iter(self._iterator)  # pragma: no cover

    def to_set(self) -> set[T]:
        return set(self._iterator)  # pragma: no cover

    ### Transformations
    def map(  # noqa: A003 # Ignore that it's shadowing a python built-in
        self,
        func: Callable[[T], S],
    ) -> "Iter[S]":
        return Iter(map(func, self._iterator))

    def pmap(
        self,
        func: Callable[[T], S],
    ) -> "Iter[S]":
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        with multiprocessing.Pool() as pool:
            return Iter(pool.map(func, self._iterator))

    def filter(self, func: Callable[[T], bool]) -> "Iter[T]":  # noqa: A003
        return Iter(filter(func, self._iterator))

    def groupby(
        self, func: Callable[[T], str]
    ) -> "Iter[tuple[str, list[T]]]":
        groups_with_values: defaultdict[str, list[T]] = defaultdict(
            list
        )

        for value in self._iterator:
            value_key = func(value)
            groups_with_values[value_key].append(value)

        tuples = list(groups_with_values.items())
        return Iter(tuples)

    def flatten(self) -> "Iter[T]":
        values: list[T] = []
        for i in self._iterator:
            if isinstance(i, Sequence) and not isinstance(i, str):
                values.extend(i)
            else:
                values.append(i)

        return Iter(values)
