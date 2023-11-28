from functionalpy._sequence import Seq


# TODO: https://github.com/MartinBernstorff/FunctionalPy/issues/40 tests: add hypothesis tests where it makes sense
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


class TestGroupby:
    def test_grouped_filter(self):
        sequence = Seq([1, 2, 3, 4])

        def is_even(num: int) -> str:
            if num % 2 == 0:
                return "even"
            return "odd"

        grouped = sequence.groupby(is_even)
        assert grouped == {
            "odd": [1, 3],
            "even": [2, 4],
        }

    def test_grouped_map(self):
        ...

    def test_grouped_reduce(self):
        ...


def test_flatten():
    test_input = ((1, 2), (3, 4))
    sequence = Seq(test_input)
    result = sequence.flatten()
    assert result.to_list() == [1, 2, 3, 4]


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
