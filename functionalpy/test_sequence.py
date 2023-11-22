from dataclasses import dataclass

from functionalpy._sequence import Seq


def test_chaining():
    sequence = Seq([1, 2])
    result = (
        sequence.filter(lambda x: x % 2 == 0)
        .map(lambda x: x * 2)
        .to_list()
    )
    assert result == [4]


def test_map():
    sequence = Seq([1, 2])
    result = sequence.map(lambda x: x * 2).to_list()
    assert result == [2, 4]


def test_filter():
    sequence = Seq((1, 2))
    result = sequence.filter(lambda x: x % 2 == 0).to_list()
    assert result == [2]


def test_reduce():
    sequence = Seq([1, 2])
    result = sequence.reduce(lambda x, y: x + y)
    assert result == 3


def test_flatten():
    test_input = ((1, 2), (3, 4))
    sequence = Seq(test_input)
    result = sequence.flatten()
    assert result.to_list() == [1, 2, 3, 4]


@dataclass(frozen=True)
class GroupbyInput:
    key: str
    value: int


# TODO: Properly specify groupby
# Some desirable properties:
# - Direct indexing by group key
# - Still a sequence we can use .map etc. on
def test_groupby():
    groupby_inputs = [
        GroupbyInput(key="a", value=1),
        GroupbyInput(key="a", value=2),
        GroupbyInput(key="b", value=3),
    ]
    sequence = Seq(groupby_inputs)
    result = sequence.groupby(lambda x: x.key).to_tuple()

    assert len(result) == 2
    assert [x.key for x in result] == ["a", "b"]
    assert [x.value.to_list() for x in result if x.key == "a"] == [
        (1, 2)
    ]
    assert [x.value.to_list() for x in result if x.key == "b"] == [
        (3,)
    ]


class TestFlattenTypes:
    def test_flatten_tuple(self):
        test_input = ((1, 2), (3, 4))
        sequence = Seq(test_input)
        result = sequence.flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_list(self):
        test_input = [[1, 2], [3, 4]]
        sequence = Seq(test_input)
        result = sequence.flatten()
        assert result.to_list() == [1, 2, 3, 4]

    def test_flatten_str(self):
        test_input = ["abcd"]
        sequence = Seq(test_input)
        result = sequence.flatten()
        assert result.to_list() == ["a", "b", "c", "d"]
