import pytest
from extenum import ImplicitEnum


class SimpleNumbers1(ImplicitEnum):
    ONE
    TWO
    THREE


class SimpleNumbers2(ImplicitEnum):
    ONE, TWO, THREE


class MixedExplicitEnum1(ImplicitEnum):
    ONE
    TWO = 2
    THREE


class MixedExplicitEnum2(ImplicitEnum):
    ONE = 1
    TWO
    THREE = 3


class MixedExplicitEnum3(ImplicitEnum):
    ONE = 1
    TWO = 2
    THREE


class DuplicatedValueWithExplicitEnum(ImplicitEnum):
    ONE
    TWO = 1
    THREE = 1


@pytest.mark.parametrize(('enum', 'expected'), [
    (SimpleNumbers1, [('ONE', 1), ('TWO', 2), ('THREE', 3)]),
    (SimpleNumbers2, [('ONE', 1), ('TWO', 2), ('THREE', 3)]),
    (MixedExplicitEnum1, [('ONE', 1), ('TWO', 2), ('THREE', 3)]),
    (MixedExplicitEnum2, [('ONE', 1), ('TWO', 2), ('THREE', 3)]),
    (MixedExplicitEnum3, [('ONE', 1), ('TWO', 2), ('THREE', 3)]),
    (DuplicatedValueWithExplicitEnum, [('ONE', 1), ('TWO', 1), ('THREE', 1)]),
], ids=[
    'SimpleNumbers1',
    'SimpleNumbers2',
    'MixedExplicitEnum1',
    'MixedExplicitEnum2',
    'MixedExplicitEnum3',
    'DuplicatedValueWithExplicitEnum',
])
def test_simple_implicit_enum(enum, expected):
    iterable = zip(enum.__members__.items(), expected)
    for (name, const), (exp_name, exp_value) in iterable:
        assert name == exp_name
        assert const.value == exp_value
