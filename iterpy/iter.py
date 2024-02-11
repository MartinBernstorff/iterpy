import multiprocessing
from collections import defaultdict
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Sequence,
)
from functools import reduce
from itertools import islice
from typing import Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")
Predicate = Callable[[T], bool]
Reducer = Callable[[T, T], T]
Mapper = Callable[[T], S]
Hasher = Callable[[T], str]


class Iter(Generic[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        self._nonconsumable_iterable: list[T] = list(iterable)
        self._current_index: int = 0

    @property
    def _iterator(self) -> Iterator[T]:
        return iter(self._nonconsumable_iterable)

    def __iter__(self) -> "Iter[T]":
        return self

    def __next__(self) -> T:
        try:
            item = self._nonconsumable_iterable[self._current_index]
        except IndexError:
            raise StopIteration  # noqa: B904
        self._current_index += 1
        return item

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

    def __repr__(self) -> str:
        return f"Iter{self._nonconsumable_iterable}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Iter):
            return False
        return (
            self._nonconsumable_iterable
            == other._nonconsumable_iterable
        )

    ### Reductions
    def reduce(self, func: Reducer) -> T:
        return reduce(func, self._iterator)

    def count(self) -> int:
        return sum(1 for _ in self._iterator)

    ### Output
    def to_list(self) -> list[T]:
        return self._nonconsumable_iterable

    def to_tuple(self) -> tuple[T, ...]:
        return tuple(self._iterator)  # pragma: no cover

    def to_consumable(self) -> Iterator[T]:
        return iter(self._iterator)  # pragma: no cover

    def to_set(self) -> set[T]:
        return set(self._iterator)  # pragma: no cover

    ### Transformations
    def map(  # Ignore that it's shadowing a python built-in
        self, func: Callable[[T], S]
    ) -> "Iter[S]":
        return Iter([func(i) for i in self._iterator])

    def pmap(
        self,
        func: Callable[[T], S],
    ) -> "Iter[S]":
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        with multiprocessing.Pool() as pool:
            return Iter(pool.map(func, self._iterator))

    def filter(self, func: Predicate) -> "Iter[T]":
        return Iter([i for i in self._iterator if func(i)])

    def groupby(self, func: Hasher) -> "Iter[tuple[str, list[T]]]":
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
            elif isinstance(i, Iter):
                values.extend(i.to_list())
            else:
                values.append(i)

        return Iter(values)

    def take(self, n: int = 1) -> "Iter[T]":
        return Iter(self._nonconsumable_iterable[0:n])

    def rev(self) -> "Iter[T]":
        return Iter(reversed(self._nonconsumable_iterable))

    def any(self, func: Predicate) -> bool:
        return any(func(i) for i in self._iterator)

    def all(self, func: Predicate) -> bool:
        return all(func(i) for i in self._iterator)

    def unique(self) -> "Iter[T]":
        return Iter(set(self._iterator))

    def unique_by(self, func: Callable[[T], S]) -> "Iter[T]":
        seen: set[S] = set()
        values: list[T] = []

        for value in self._iterator:
            key = func(value)
            if key not in seen:
                seen.add(key)
                values.append(value)

        return Iter(values)

    def enumerate(self) -> "Iter[tuple[int, T]]":
        return Iter(enumerate(self._iterator))

    def find(self, func: Predicate) -> T | None:
        for value in self._iterator:
            if func(value):
                return value
        return None

    def last(self) -> T:
        return self._nonconsumable_iterable[-1]
