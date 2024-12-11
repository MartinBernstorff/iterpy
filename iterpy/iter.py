from __future__ import annotations

import copy
import multiprocessing
from collections import defaultdict
from functools import reduce
from itertools import islice
from typing import TYPE_CHECKING, Any, Generator, Generic, Sequence, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from iterpy.arr import Arr

T = TypeVar("T")
S = TypeVar("S")


class Iter(Generic[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        self._iter = iter(iterable)
        self._current_index: int = 0

    @property
    def _iterator(self) -> Iterator[T]:
        return iter(self._iter)

    def __bool__(self) -> bool:
        return bool(self._iter)

    def __iter__(self) -> Iter[T]:
        return self

    def __next__(self) -> T:
        return next(self._iter)

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> Iter[T]: ...

    def __getitem__(self, index: int | slice) -> T | Iter[T]:
        if isinstance(index, int) and index >= 0:
            try:
                return next(islice(self._iter, index, index + 1))
            except StopIteration:
                raise IndexError("Index out of range") from None
        elif isinstance(index, slice):
            return Iter(islice(self._iterator, index.start, index.stop, index.step))
        else:
            raise KeyError(f"Key must be non-negative integer or slice, not {index}")

    def __repr__(self) -> str:
        return f"Iter{self._iter}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Iter):
            return False
        return self._iter == other._iter  # type: ignore

    ### Reductions
    def reduce(self, func: Callable[[T, T], T]) -> T:
        return reduce(func, self._iterator)

    def count(self) -> int:
        return sum(1 for _ in self._iterator)

    ### Output
    def to_list(self) -> list[T]:
        return list(self._iter)

    def to_tuple(self) -> tuple[T, ...]:
        return tuple(self._iterator)  # pragma: no cover

    def to_set(self) -> set[T]:
        return set(self._iterator)  # pragma: no cover

    def collect(self) -> Arr[T]:
        from iterpy.arr import Arr

        return Arr(self._iterator)

    ### Transformations
    def map(  # Ignore that it's shadowing a python built-in
        self, func: Callable[[T], S]
    ) -> Iter[S]:
        return Iter(map(func, self._iterator))

    def pmap(self, func: Callable[[T], S]) -> Iter[S]:
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        with multiprocessing.Pool() as pool:
            return Iter(pool.map(func, self._iterator))

    def filter(self, func: Callable[[T], bool]) -> Iter[T]:
        return Iter(filter(func, self._iterator))  # type: ignore

    def groupby(self, func: Callable[[T], str]) -> Iter[tuple[str, list[T]]]:
        groups_with_values: defaultdict[str, list[T]] = defaultdict(list)

        for value in self._iterator:
            value_key = func(value)
            groups_with_values[value_key].append(value)

        tuples = list(groups_with_values.items())
        return Iter(tuples)

    def take(self, n: int = 1) -> Iter[T]:
        return Iter(islice(self._iter, n))

    def any(self, func: Callable[[T], bool]) -> bool:
        return any(func(i) for i in self._iterator)

    def all(self, func: Callable[[T], bool]) -> bool:
        return all(func(i) for i in self._iterator)

    def unique(self) -> Iter[T]:
        return Iter(set(self._iterator))

    def unique_by(self, func: Callable[[T], S]) -> Iter[T]:
        seen: set[S] = set()
        values: list[T] = []

        for value in self._iterator:
            key = func(value)
            if key not in seen:
                seen.add(key)
                values.append(value)

        return Iter(values)

    def enumerate(self) -> Iter[tuple[int, T]]:
        return Iter(enumerate(self._iterator))

    def find(self, func: Callable[[T], bool]) -> T | None:
        for value in self._iterator:
            if func(value):
                return value
        return None

    def clone(self) -> Iter[T]:
        return copy.deepcopy(self)

    def zip(self, other: Iter[S]) -> Iter[tuple[T, S]]:
        return Iter(zip(self, other))

    ############################################################
    # Auto-generated overloads for flatten                     #
    # Code for generating the following is in _generate_pyi.py #
    ############################################################
    # Overloads are technically incompatible, because they use generic S instead of T. However, this is required for the flattening logic to work.

    @overload
    def flatten(self: Iter[Iterable[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[Iterable[S] | S]) -> Iter[S]: ...

    # Iterator[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[Iterator[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[Iterator[S] | S]) -> Iter[S]: ...

    # tuple[S, ...]   # noqa: ERA001
    @overload
    def flatten(self: Iter[tuple[S, ...]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[tuple[S, ...] | S]) -> Iter[S]: ...

    # Sequence[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[Sequence[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[Sequence[S] | S]) -> Iter[S]: ...

    # list[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[list[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[list[S] | S]) -> Iter[S]: ...

    # set[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[set[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[set[S] | S]) -> Iter[S]: ...

    # frozenset[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[frozenset[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[frozenset[S] | S]) -> Iter[S]: ...

    # Iter[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[Iter[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[Iter[S] | S]) -> Iter[S]: ...

    # str
    @overload
    def flatten(self: Iter[str]) -> Iter[str]: ...
    @overload
    def flatten(self: Iter[str | S]) -> Iter[S]: ...

    # Generic
    @overload
    def flatten(self: Iter[S]) -> Iter[S]: ...

    def flatten(self) -> Iter[T]:  # type: ignore -
        depth = 1

        def walk(node: Any, level: int) -> Generator[T, None, None]:
            if (level > depth) or isinstance(node, str):
                yield node  # type: ignore
                return
            try:
                tree = iter(node)
            except TypeError:
                yield node
                return
            else:
                for child in tree:
                    yield from walk(child, level + 1)

        return Iter(walk(self, level=0))  # type: ignore
