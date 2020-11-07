from enum import Enum

import pytest
from extenum import EnumSet


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    @classmethod
    def set_of(cls, values):
        opts = EnumSet.none_of(cls)
        for value in values:
            opts.add(cls(value))
        return opts


class YetAnotherNumber(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class NonEnum:
    pass


def assert_constant(names, values, enumset):
    for const in enumset:
        assert const.name in names
        assert const.value in values


def test_enum_set_of():
    enumset = Number.set_of([1, 3, 5])
    assert len(enumset) == 3
    names, values = ('ONE', 'THREE', 'FIVE'), (1, 3, 5)
    assert_constant(names, values, enumset)


def test_enumset_none_of():
    enumset = EnumSet.none_of(Number)
    assert len(enumset) == 0
    assert enumset._enum_type is Number
    enumset.add(Number.ONE)
    assert len(enumset) == 1
    enumset.add(Number.THREE)
    assert len(enumset) == 2

    names, values = ('ONE', 'THREE'), (1, 3)
    assert_constant(names, values, enumset)


def test_enumset_all_of():
    enumset = EnumSet.all_of(Number)
    assert len(enumset) == 5
    assert enumset._enum_type is Number
    assert Number.TWO in enumset
    assert YetAnotherNumber.TWO not in enumset

    names = ('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE')
    values = range(1, 6)
    assert_constant(names, values, enumset)


def test_enumset_of_one():
    enumset = EnumSet.of(Number.ONE)
    assert len(enumset) == 1
    assert enumset._enum_type is Number

    names, values = ('ONE',), (1,)
    assert_constant(names, values, enumset)


def test_enumset_of_three():
    enumset = EnumSet.of(Number.ONE, Number.THREE, Number.FIVE)
    assert len(enumset) == 3
    assert enumset._enum_type is Number

    names, values = ('ONE', 'THREE', 'FIVE'), (1, 3, 5)
    assert_constant(names, values, enumset)


def test_enumset_of_update():
    enumset1 = EnumSet.of(Number.ONE, Number.THREE, Number.FIVE)
    enumset2 = EnumSet.of(Number.ONE, Number.TWO, Number.FOUR)
    enumset1.update(enumset2)
    assert len(enumset1) == 5
    names = ('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE')
    values = range(1, 6)
    assert_constant(names, values, enumset1)

    assert len(enumset2) == 3
    enumset2.update(enumset1)
    assert len(enumset2) == 5
    assert_constant(names, values, enumset2)


def test_enumset_of_remove():
    enumset = EnumSet.of(Number.ONE, Number.THREE, Number.FIVE)
    enumset.remove(Number.THREE)
    assert len(enumset) == 2

    with pytest.raises(KeyError) as excinfo:
        enumset.remove(Number.TWO)
    assert str(excinfo.value) == '<Number.TWO: 2>'
    assert len(enumset) == 2


def test_enumset_of_discard():
    enumset = EnumSet.of(Number.ONE, Number.THREE, Number.FIVE)
    enumset.discard(Number.TWO)
    assert len(enumset) == 3
    enumset.discard(Number.FIVE)
    assert len(enumset) == 2


def test_raise_enumset_of_not_consistent_enum_type():
    with pytest.raises(ValueError) as excinfo:
        EnumSet.of(Number.ONE, YetAnotherNumber.TWO)

    expected = '(<Number.ONE: 1>, <YetAnotherNumber.TWO: 2>) '\
               'are not consistent Enum type'
    assert str(excinfo.value) == expected


def test_raise_enumset_add_not_member_of_enum():
    enumset = EnumSet.none_of(Number)
    enumset.add(Number.ONE)
    with pytest.raises(ValueError) as excinfo:
        enumset.add(YetAnotherNumber.TWO)

    expected = "<YetAnotherNumber.TWO: 2> is not member of <enum 'Number'>"
    assert str(excinfo.value) == expected


def test_raise_enumset_update_not_member_of_enum():
    yaenumset = EnumSet.none_of(YetAnotherNumber)
    yaenumset.add(YetAnotherNumber.ONE)
    enumset = EnumSet.of(Number.TWO)
    with pytest.raises(ValueError) as excinfo:
        yaenumset.update(enumset)

    expected = "<Number.TWO: 2> is not member of <enum 'YetAnotherNumber'>"
    assert str(excinfo.value) == expected


def test_enumset_range():
    enumset = EnumSet.range(Number.TWO, Number.FOUR)
    assert len(enumset) == 3
    assert enumset._enum_type is Number

    names, values = ('TWO', 'THREE', 'FOUR'), (2, 3, 4)
    assert_constant(names, values, enumset)


def test_raise_enumset_range_not_consistent_enum_type():
    with pytest.raises(ValueError) as excinfo:
        EnumSet.range(Number.TWO, YetAnotherNumber.THREE)

    expected = '(<Number.TWO: 2>, <YetAnotherNumber.THREE: 3>) '\
               'are not consistent Enum type'
    assert str(excinfo.value) == expected


def test_create_enumset():
    enumset = EnumSet(Number)
    assert len(enumset) == 0
    assert enumset._enum_type is Number
    enumset.add(Number.FOUR)
    assert len(enumset) == 1
    elem = enumset.pop()
    assert len(enumset) == 0
    assert elem.name == 'FOUR'
    assert elem.value == 4


def test_raise_is_not_enum_subtype():
    with pytest.raises(TypeError) as excinfo:
        EnumSet(NonEnum)

    expected = "<class 'test_enumset.NonEnum'> is not Enum subclass"
    assert str(excinfo.value) == expected
