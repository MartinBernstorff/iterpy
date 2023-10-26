from functionalpy.sequence import Seq


def test_chaining():
    sequence = Seq([1, 2])
    result = sequence.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).to_list()
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
    sequence = Seq([[1, 2], [3, 4]])
    result = sequence.flatten().to_list()
    assert result == [1, 2, 3, 4]
