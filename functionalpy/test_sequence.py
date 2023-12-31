from collections.abc import Mapping, Sequence
from typing import Literal

from functionalpy._sequence import Seq


def test_chaining():
    sequence = Seq([1, 2])
    result: list[int] = (
        sequence.filter(lambda x: x % 2 == 0)
        .map(lambda x: x * 2)
        .to_list()
    )
    assert result == [4]


def test_map():
    sequence = Seq([1, 2])
    result: list[int] = sequence.map(lambda x: x * 2).to_list()
    assert result == [2, 4]


def multiple_by_2(num: int) -> int:
    return num * 2  # pragma: no cover


def test_pmap():
    sequence = Seq([1, 2])
    result: list[int] = sequence.pmap(multiple_by_2).to_list()
    assert result == [2, 4]


def test_filter():
    sequence = Seq([1, 2])
    result: list[int] = sequence.filter(
        lambda x: x % 2 == 0
    ).to_list()
    assert result == [2]


def test_reduce():
    sequence = Seq([1, 2])
    result: int = sequence.reduce(lambda x, y: x + y)
    assert result == 3


def test_count():
    sequence = Seq([1, 2])
    result: int = sequence.count()
    assert result == 2


def test_grouped_filter():
    sequence = Seq([1, 2, 3, 4])

    def is_even(num: int) -> str:
        if num % 2 == 0:
            return "even"
        return "odd"

    grouped: Mapping[str, Sequence[int]] = sequence.groupby(is_even)
    assert grouped == {
        "odd": [1, 3],
        "even": [2, 4],
    }


def test_flatten():
    test_input: list[list[int]] = [[1, 2], [3, 4]]
    sequence = Seq(test_input)
    result: Seq[int] = sequence.flatten()
    assert result.to_list() == [1, 2, 3, 4]


class TestFlattenTypes:
    def test_flatten_tuple(self):
        test_input: Sequence[tuple[int, ...]] = (
            (1, 2),
            (3, 4),
        )
        sequence = Seq(test_input)
        result: Seq[Literal[1, 2, 3, 4]] = sequence.flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_list(self):
        test_input: list[list[int]] = [[1, 2], [3, 4]]
        sequence = Seq(test_input)
        result: Seq[int] = sequence.flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_sequence(self):
        test_input: Sequence[Sequence[int]] = [[1, 2], [3, 4]]
        result: Seq[int] = Seq(test_input).flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_str(self):
        test_input: list[str] = ["abcd"]
        sequence = Seq(test_input)
        result: Seq[str] = sequence.flatten()
        assert result.to_list() == ["a", "b", "c", "d"]

    def test_flatten_includes_primitives(self):
        test_input: list[int | list[int]] = [1, [2]]
        result: Seq[int] = Seq(test_input).flatten()
        assert result.to_list() == [1, 2]

    def test_flatten_removes_empty_sequences(self):
        test_input: list[list[int]] = [[1], []]
        result: Seq[int] = Seq(test_input).flatten()
        assert result.to_list() == [1]
