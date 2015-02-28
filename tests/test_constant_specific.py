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


def test_work_as_planet_enum():
    class Planet(ConstantSpecificEnum):
        MERCURY = (3.303e+23, 2.4397e6)
        VENUS = (4.869e+24, 6.0518e6)
        EARTH = (5.976e+24, 6.37814e6)
        MARS = (6.421e+23, 3.3972e6)
        JUPITER = (1.9e+27, 7.1492e7)
        SATURN = (5.688e+26, 6.0268e7)
        URANUS = (8.686e+25, 2.5559e7)
        NEPTUNE = (1.024e+26, 2.4746e7)

        overload = RegisterFactory()

        def __init__(self, mass, radius):
            self.mass = mass       # in kilograms
            self.radius = radius   # in meters

        @property
        def surface_gravity(self):
            # universal gravitational constant  (m3 kg-1 s-2)
            G = 6.67300E-11
            return G * self.mass / (self.radius * self.radius)

        @overload.register(MERCURY)
        def name(self):
            return 'MERCURY'

        @overload.register(VENUS)
        def name(self):
            return 'VENUS'

        @overload.register(EARTH)
        def name(self):
            return 'EARTH'

        @overload.register(MARS)
        def name(self):
            return 'MARS'

        @overload.register(JUPITER)
        def name(self):
            return 'JUPITER'

        @overload.register(SATURN)
        def name(self):
            return 'SATURN'

        @overload.register(URANUS)
        def name(self):
            return 'URANUS'

        @overload.register(NEPTUNE)
        def name(self):
            return 'NEPTUNE'

    assert Planet.EARTH.value == (5.976e+24, 6378140.0)
    assert Planet.EARTH.surface_gravity == 9.802652743337129
    for name, const in Planet.__members__.items():
        assert name == const.name()
