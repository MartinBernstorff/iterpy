import multiprocessing
from collections import defaultdict
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
from functools import reduce
from typing import Generic, TypeVar

from click import group

_T = TypeVar("_T")
_S = TypeVar("_S")


class Seq(Generic[_T]):
    def __init__(self, iterable: Iterable[_T]):
        self._seq = iterable

    ### Reductions
    def count(self) -> int:
        return sum(1 for _ in self._seq)

    ### Output
    def to_list(self) -> list[_T]:
        return list(self._seq)

    def to_tuple(self) -> tuple[_T, ...]:
        return tuple(self._seq)  # pragma: no cover

    def to_iter(self) -> Iterator[_T]:
        return iter(self._seq)  # pragma: no cover

    def to_set(self) -> set[_T]:
        return set(self._seq)  # pragma: no cover

    ### Transformations
    def map(  # noqa: A003 # Ignore that it's shadowing a python built-in
        self,
        func: Callable[[_T], _S],
    ) -> "Seq[_S]":
        return Seq(map(func, self._seq))

    def pmap(
        self,
        func: Callable[[_T], _S],
    ) -> "Seq[_S]":
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        with multiprocessing.Pool() as pool:
            return Seq(pool.map(func, self._seq))

    def filter(self, func: Callable[[_T], bool]) -> "Seq[_T]":  # noqa: A003
        return Seq(filter(func, self._seq))

    def reduce(self, func: Callable[[_T, _T], _T]) -> _T:
        return reduce(func, self._seq)

    def groupby(
        self, func: Callable[[_T], str]
    ) -> "Seq[tuple[str, list[_T]]]":
        groups_with_values: defaultdict[str, list[_T]] = defaultdict(
            list
        )

        for value in self._seq:
            value_key = func(value)
            groups_with_values[value_key].append(value)

        tuples = list(groups_with_values.items())
        return Seq(tuples)

    def flatten(self) -> "Seq[_T]":
        values: list[_T] = []

        for i in self._seq:
            if isinstance(i, Sequence) and not isinstance(i, str):
                values.extend(i)
            else:
                values.append(i)

        return Seq(values)
