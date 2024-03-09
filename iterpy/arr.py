from __future__ import annotations

import copy
import multiprocessing
from collections import defaultdict
from functools import reduce
from itertools import islice
from typing import TYPE_CHECKING, Any, Generator, Generic, Sequence, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

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
        return bool(self._iter)

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
        return reduce(func, self._iterator)

    def count(self) -> int:
        return sum(1 for _ in self._iterator)

    ### Output
    def to_list(self) -> list[T]:
        return list(self._iter)

    def to_tuple(self) -> tuple[T, ...]:
        return tuple(self._iterator)  # pragma: no cover

    def to_consumable(self) -> Iterator[T]:
        return iter(self._iterator)  # pragma: no cover

    def to_set(self) -> set[T]:
        return set(self._iterator)  # pragma: no cover

    ### Transformations
    def map(  # Ignore that it's shadowing a python built-in
        self, func: Callable[[T], S]
    ) -> Arr[S]:
        return Arr(map(func, self._iterator))

    def pmap(self, func: Callable[[T], S]) -> Arr[S]:
        """Parallel map using multiprocessing.Pool

        Not that lambdas are not supported by multiprocessing.Pool.map.
        """
        with multiprocessing.Pool() as pool:
            return Arr(pool.map(func, self._iterator))

    def filter(self, func: Callable[[T], bool]) -> Arr[T]:
        return Arr(filter(func, self._iterator))  # type: ignore

    def groupby(self, func: Callable[[T], str]) -> Arr[tuple[str, list[T]]]:
        groups_with_values: defaultdict[str, list[T]] = defaultdict(list)

        for value in self._iterator:
            value_key = func(value)
            groups_with_values[value_key].append(value)

        tuples = list(groups_with_values.items())
        return Arr(tuples)

    def take(self, n: int = 1) -> Arr[T]:
        return Arr(islice(self._iter, n))

    def any(self, func: Callable[[T], bool]) -> bool:
        return any(func(i) for i in self._iterator)

    def all(self, func: Callable[[T], bool]) -> bool:
        return all(func(i) for i in self._iterator)

    def unique(self) -> Arr[T]:
        return Arr(set(self._iterator))

    def unique_by(self, func: Callable[[T], S]) -> Arr[T]:
        seen: set[S] = set()
        values: list[T] = []

        for value in self._iterator:
            key = func(value)
            if key not in seen:
                seen.add(key)
                values.append(value)

        return Arr(values)

    def enumerate(self) -> Arr[tuple[int, T]]:
        return Arr(enumerate(self._iterator))

    def find(self, func: Callable[[T], bool]) -> T | None:
        for value in self._iterator:
            if func(value):
                return value
        return None

    def clone(self) -> Arr[T]:
        return copy.deepcopy(self)

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

    def flatten(self) -> Arr[T]:  # type: ignore -
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

        return Arr(walk(self, level=0))  # type: ignore
