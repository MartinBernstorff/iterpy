from functools import reduce
from typing import Callable, Generic, Iterable, Iterator, Sequence, TypeVar

_ContainedType = TypeVar("_ContainedType")
_T1 = TypeVar("_T1")


class Seq(Generic[_ContainedType]):
    def __init__(self, iterable: Iterable[_ContainedType]):
        self._seq = iterable

    def to_list(self) -> list[_ContainedType]:
        return list(self._seq)

    def to_generator(self) -> Iterator[_ContainedType]:
        return (i for i in self._seq)

    def map(self, func: Callable[[_ContainedType], _T1]) -> "Seq[_T1]":  # noqa: A003
        return Seq(map(func, self._seq))

    def filter(  # noqa: A003
        self, func: Callable[[_ContainedType], bool]
    ) -> "Seq[_ContainedType]":
        return Seq(filter(func, self._seq))

    def reduce(
        self, func: Callable[[_ContainedType, _ContainedType], _ContainedType]
    ) -> _ContainedType:
        return reduce(func, self._seq)

    def flatten(self) -> "Seq[_ContainedType]":
        return Seq(
            (
                item
                for sublist in self._seq
                for item in sublist
                if isinstance(sublist, Sequence)
            )
        )
