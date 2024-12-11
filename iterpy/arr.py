from __future__ import annotations

from itertools import islice
from typing import TYPE_CHECKING, Generic, Sequence, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from iterpy.iter import Iter

T = TypeVar("T")
S = TypeVar("S")


class Arr(Generic[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        self._iter = list(iterable)
        self._current_index: int = 0

    @property
    def _iterator(self) -> Iterator[T]:
        return iter(self._iter)

    def __bool__(self) -> bool:
        return self.lazy().__bool__()

    def __iter__(self) -> Arr[T]:
        return self

    def __next__(self) -> T:
        try:
            item = self._iter[self._current_index]
        except IndexError:
            raise StopIteration  # noqa: B904
        self._current_index += 1
        return item

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> Arr[T]: ...

    def __getitem__(self, index: int | slice) -> T | Arr[T]:
        if isinstance(index, int) and index >= 0:
            try:
                return next(islice(self._iter, index, index + 1))
            except StopIteration:
                raise IndexError("Index out of range") from None
        elif isinstance(index, slice):
            return Arr(islice(self._iterator, index.start, index.stop, index.step))
        else:
            raise KeyError(f"Key must be non-negative integer or slice, not {index}")

    def __repr__(self) -> str:
        return f"Arr{self._iter}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Arr):
            return False
        return self._iter == other._iter  # type: ignore

    ### Reductions
    def reduce(self, func: Callable[[T, T], T]) -> T:
        return self.lazy().reduce(func)

    def count(self) -> int:
        return self.lazy().count()

    ### Output
    def to_list(self) -> list[T]:
        return self.lazy().to_list()

    def to_tuple(self) -> tuple[T, ...]:
        return self.lazy().to_tuple()

    def to_set(self) -> set[T]:
        return self.lazy().to_set()

    def lazy(self) -> Iter[T]:
        from iterpy.iter import Iter

        return Iter(self._iterator)

    ### Transformations
    def map(  # Ignore that it's shadowing a python built-in
        self, func: Callable[[T], S]
    ) -> Arr[S]:
        return self.lazy().map(func).collect()

    def pmap(self, func: Callable[[T], S]) -> Arr[S]:
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        return self.lazy().pmap(func).collect()

    def filter(self, func: Callable[[T], bool]) -> Arr[T]:
        return self.lazy().filter(func).collect()

    def groupby(self, func: Callable[[T], str]) -> Arr[tuple[str, list[T]]]:
        return self.lazy().groupby(func).collect()

    def take(self, n: int = 1) -> Arr[T]:
        return self.lazy().take(n).collect()

    def any(self, func: Callable[[T], bool]) -> bool:
        return self.lazy().any(func)

    def all(self, func: Callable[[T], bool]) -> bool:
        return self.lazy().all(func)

    def unique(self) -> Arr[T]:
        return self.lazy().unique().collect()

    def unique_by(self, func: Callable[[T], S]) -> Arr[T]:
        return self.lazy().unique_by(func).collect()

    def enumerate(self) -> Arr[tuple[int, T]]:
        return self.lazy().enumerate().collect()

    def find(self, func: Callable[[T], bool]) -> T | None:
        return self.lazy().find(func)

    def clone(self) -> Arr[T]:
        return self.lazy().clone().collect()

    def zip(self, other: Arr[S]) -> Arr[tuple[T, S]]:
        return Arr(zip(self, other))

    ############################################################
    # Auto-generated overloads for flatten                     #
    # Code for generating the following is in _generate_pyi.py #
    ############################################################
    # Overloads are technically incompatible, because they use generic S instead of T. However, this is required for the flattening logic to work.

    @overload
    def flatten(self: Arr[Iterable[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[Iterable[S] | S]) -> Arr[S]: ...

    # Iterator[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[Iterator[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[Iterator[S] | S]) -> Arr[S]: ...

    # tuple[S, ...]   # noqa: ERA001
    @overload
    def flatten(self: Arr[tuple[S, ...]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[tuple[S, ...] | S]) -> Arr[S]: ...

    # Sequence[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[Sequence[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[Sequence[S] | S]) -> Arr[S]: ...

    # list[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[list[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[list[S] | S]) -> Arr[S]: ...

    # set[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[set[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[set[S] | S]) -> Arr[S]: ...

    # frozenset[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[frozenset[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[frozenset[S] | S]) -> Arr[S]: ...

    # Arr[S]   # noqa: ERA001
    @overload
    def flatten(self: Arr[Arr[S]]) -> Arr[S]: ...
    @overload
    def flatten(self: Arr[Arr[S] | S]) -> Arr[S]: ...

    # str
    @overload
    def flatten(self: Arr[str]) -> Arr[str]: ...
    @overload
    def flatten(self: Arr[str | S]) -> Arr[S]: ...

    # Generic
    @overload
    def flatten(self: Arr[S]) -> Arr[S]: ...

    def flatten(self) -> Arr[T]:  # type: ignore
        return self.lazy().flatten().collect()
