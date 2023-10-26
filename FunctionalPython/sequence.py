import itertools
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from functools import reduce
from typing import Generic, TypeVar

_T0 = TypeVar("_T0")
_T1 = TypeVar("_T1")


@dataclass(frozen=True)
class Group(Generic[_T0]):
    group_id: str
    group_contents: "Seq[_T0]"


class Seq(Generic[_T0]):
    def __init__(self, iterable: Iterable[_T0]):
        self._seq = iterable

    ### Reductions
    def count(self) -> int:
        return sum(1 for _ in self._seq)

    ### Output
    def to_list(self) -> list[_T0]:
        return list(self._seq)

    def to_tuple(self) -> tuple[_T0, ...]:
        return tuple(self._seq)

    def to_iter(self) -> Iterator[_T0]:
        return iter(self._seq)

    def to_set(self) -> set[_T0]:
        return set(self._seq)

    ### Transformations
    def map(  # noqa: A003 # Ignore that it's shadowing a python built-in
        self,
        func: Callable[[_T0], _T1],
    ) -> "Seq[_T1]":
        return Seq(map(func, self._seq))

    def filter(self, func: Callable[[_T0], bool]) -> "Seq[_T0]":  # noqa: A003
        return Seq(filter(func, self._seq))

    def reduce(self, func: Callable[[_T0, _T0], _T0]) -> _T0:
        return reduce(func, self._seq)

    def group_by(self, func: Callable[[_T0], str]) -> "Seq[Group[_T0]]":
        result = (
            Group(group_id=key, group_contents=Seq(value))
            for key, value in itertools.groupby(self._seq, key=func)
        )
        return Seq(result)

    def flatten(self) -> "Seq[_T0]":
        return Seq(
            item
            for sublist in self._seq
            for item in sublist  # type: ignore
            if isinstance(sublist, Sequence)
        )
