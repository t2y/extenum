# -*- coding: utf-8 -*-
from operator import methodcaller

import pytest
from extenum import ConstantSpecificEnum, RegisterFactory


def test_constant_specific_method():
    class TestEnum(ConstantSpecificEnum):
        ONE = 1
        TWO = 2

        overload = RegisterFactory()

        @property
        @overload.register(ONE)
        def alias(self):
            return 'alias {}'.format(self.name)

        @property
        @overload.register(TWO)
        def alias(self):
            return 'alias {}'.format(self.name)

        @overload.register(ONE)
        def is_one(self):
            return True

        @overload.register(ONE)
        def is_two(self):
            return False

        @overload.register(TWO)
        def is_one(self):
            return False

        @overload.register(TWO)
        def is_two(self):
            return True

        def get_common(self):
            return 'common'

    assert getattr(TestEnum, 'overload', None) is None
    members = list(iter(TestEnum.__members__.keys()))
    for name, const in TestEnum.__members__.items():
        assert 'alias {}'.format(name) == const.alias
        for mname in members:
            actual = methodcaller('is_{}'.format(mname.lower()))(const)
            expected = True if name == mname else False
            assert actual is expected
        assert 'common' == const.get_common()


def test_raise_const_is_not_registered():
    with pytest.raises(ValueError) as excinfo:
        class TestEnum(ConstantSpecificEnum):
            ONE = 1
            TWO = 2

            overload = RegisterFactory()

            @overload.register(ONE)
            def test(self): pass

    expected = '<TestEnum.TWO: 2> is not registered'
    assert str(excinfo.value) == expected


def test_raise_function_is_not_registered():
    with pytest.raises(ValueError) as excinfo:
        class TestEnum(ConstantSpecificEnum):
            ONE = 1
            TWO = 2

            overload = RegisterFactory()

            @overload.register(ONE)
            def one(self): pass

            @overload.register(TWO)
            def one(self): pass

            @overload.register(TWO)
            def two(self): pass

    expected = '<TestEnum.ONE: 1>.two function is not registered'
    assert str(excinfo.value) == expected


def test_work_as_normal_enum():
    members = 'ant bee cat dog'
    Animal = ConstantSpecificEnum('Animal', members)
    assert len(members.split()) == len(list(Animal))
    for i, member in enumerate(members.split(), 1):
        const = Animal.__members__.get(member)
        assert const is not None
        assert const.name == member
        assert const.value == i
