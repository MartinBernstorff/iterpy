from collections import defaultdict
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
from dataclasses import dataclass
from functools import reduce
from typing import Generic, TypeVar

_T = TypeVar("_T")
_S = TypeVar("_S")


@dataclass(frozen=True)
class Group(Generic[_T]):
    key: str
    value: "Seq[_T]"


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

    def filter(self, func: Callable[[_T], bool]) -> "Seq[_T]":  # noqa: A003
        return Seq(filter(func, self._seq))

    def reduce(self, func: Callable[[_T, _T], _T]) -> _T:
        return reduce(func, self._seq)

    def groupby(
        self, func: Callable[[_T], str]
    ) -> "Mapping[str, Sequence[_T]]":
        mapping: defaultdict[str, list[_T]] = defaultdict(list)

        for item in self._seq:
            mapping[func(item)].append(item)

        return dict(mapping)

    def flatten(self) -> "Seq[_T]":
        return Seq(
            item
            for sublist in self._seq
            for item in sublist  # type: ignore
            if isinstance(sublist, Sequence)
        )
