from typing import Callable, Generic, Iterable, Sequence, TypeVar

_ContainedType = TypeVar("_ContainedType")
_T1 = TypeVar("_T1")


class Seq(Generic[_ContainedType]):
    def __init__(self, iterable: Iterable[_ContainedType]):
        self._seq = iterable

    def to_list(self) -> list[_ContainedType]:
        return list(self._seq)

    def to_iter(self) -> Iterable[_ContainedType]:
        return self._seq

    def map(self, func: Callable[[_ContainedType], _T1]) -> "Seq[_T1]":  # noqa: A003
        return Seq(map(func, self._seq))
