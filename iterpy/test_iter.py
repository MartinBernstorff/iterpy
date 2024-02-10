from collections.abc import Sequence

from iterpy._iter import Iter


def test_chaining():
    iterator = Iter([1, 2])
    result: list[int] = (
        iterator.filter(lambda x: x % 2 == 0)
        .map(lambda x: x * 2)
        .to_list()
    )
    assert result == [4]


def test_map():
    iterator = Iter([1, 2])
    result: list[int] = iterator.map(lambda x: x * 2).to_list()
    assert result == [2, 4]


def multiple_by_2(num: int) -> int:
    return num * 2  # pragma: no cover


def test_pmap():
    iterator = Iter([1, 2])
    result: list[int] = iterator.pmap(multiple_by_2).to_list()
    assert result == [2, 4]


def test_filter():
    iterator = Iter([1, 2])
    result: list[int] = iterator.filter(
        lambda x: x % 2 == 0
    ).to_list()
    assert result == [2]


def test_reduce():
    iterator = Iter([1, 2])
    result: int = iterator.reduce(lambda x, y: x + y)
    assert result == 3


def test_count():
    iterator = Iter([1, 2])
    result: int = iterator.count()
    assert result == 2


def test_grouped_filter():
    iterator = Iter([1, 2, 3, 4])

    def is_even(num: int) -> str:
        if num % 2 == 0:
            return "even"
        return "odd"

    grouped: list[tuple[str, list[int]]] = iterator.groupby(
        is_even
    ).to_list()
    assert grouped == [
        ("odd", [1, 3]),
        ("even", [2, 4]),
    ]


def test_getitem():
    test_input = [1, 2, 3]
    test_iterator = Iter(test_input)
    assert test_iterator[0] == 1
    assert test_iterator[0:2].to_list() == [1, 2]


def test_iteration():
    test_iterator = Iter([1, 2, 3])
    for i in test_iterator.to_consumable():
        assert i in [1, 2, 3]


def test_statefulness():
    """Iterators are stateful, so we need to make sure that we don't exhaust them"""
    test_iterator = Iter([1, 2, 3])
    assert test_iterator.to_list() == [1, 2, 3]
    assert test_iterator.to_list() == [1, 2, 3]


def test_head():
    test_iterator = Iter([1, 2, 3])
    assert test_iterator.head(2) == Iter([1, 2])


def test_tail():
    test_iterator = Iter([1, 2, 3])
    assert test_iterator.tail(2) == Iter([2, 3])


def test_flatten():
    test_input: list[list[int]] = [[1, 2], [3, 4]]
    iterator = Iter(test_input)
    result: Iter[int] = iterator.flatten()
    assert result.to_list() == [1, 2, 3, 4]


class TestFlattenTypes:
    """Intentionally not parametrised so we can manually specify the return type hints and they can be checked by pyright"""

    def test_flatten_generator(self):
        iterator: Iter[tuple[int, int]] = Iter(
            (i, i + 1) for i in range(1, 3)
        )
        result: Iter[int] = iterator.flatten()
        assert result.to_list() == [1, 2, 2, 3]

    def test_flatten_tuple(self):
        iterator: Iter[tuple[int, int]] = Iter(
            (i, i + 1) for i in range(1, 3)
        )
        result: Iter[int] = iterator.flatten()
        assert result.to_list() == [1, 2, 2, 3]

    def test_flatten_list(self):
        test_input: list[list[int]] = [[1, 2], [3, 4]]
        iterator = Iter(test_input)
        result: Iter[int] = iterator.flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_iterator(self):
        test_input: Sequence[Sequence[int]] = [[1, 2], [3, 4]]
        result: Iter[int] = Iter(test_input).flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_iter_iter(self):
        iterator: Iter[int] = Iter([1, 2])
        nested_iter: Iter[Iter[int]] = Iter([iterator])
        unnested_iter: Iter[int] = nested_iter.flatten()
        assert unnested_iter.to_list() == [1, 2]

    def test_flatten_str(self):
        test_input: list[str] = ["abcd"]
        iterator = Iter(test_input)
        result: Iter[str] = iterator.flatten()
        assert result.to_list() == ["abcd"]

    def test_flatten_includes_primitives(self):
        test_input: list[str | list[int] | None] = [
            "first",
            [2],
            None,
        ]
        result: Iter[int | str | None] = Iter(test_input).flatten()
        assert result.to_list() == ["first", 2, None]

    def test_flatten_removes_empty_iterators(self):
        test_input: list[list[int]] = [[1], []]
        result: Iter[int] = Iter(test_input).flatten()
        assert result.to_list() == [1]
