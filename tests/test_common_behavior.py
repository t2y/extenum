import pytest

from extenum import ConstantSpecificEnum
from extenum import ImplicitEnum


@pytest.mark.parametrize('enum_cls', [
    ConstantSpecificEnum,
    ImplicitEnum,
], ids=[
    'ConstantSpecificEnum',
    'ImplicitEnum',
])
def test_work_as_normal_enum(enum_cls):
    members = 'ant bee cat dog'
    Animal = enum_cls('Animal', members)
    assert len(members.split()) == len(list(Animal))
    for i, member in enumerate(members.split(), 1):
        const = Animal.__members__.get(member)
        assert const is not None
        assert const.name == member
        assert const.value == i


@pytest.mark.parametrize('enum_cls', [
    ConstantSpecificEnum,
    ImplicitEnum,
], ids=[
    'ConstantSpecificEnum',
    'ImplicitEnum',
])
def test_work_as_planet_enum(enum_cls):
    class Planet(enum_cls):
        MERCURY = (3.303e+23, 2.4397e6)
        VENUS = (4.869e+24, 6.0518e6)
        EARTH = (5.976e+24, 6.37814e6)
        MARS = (6.421e+23, 3.3972e6)
        JUPITER = (1.9e+27, 7.1492e7)
        SATURN = (5.688e+26, 6.0268e7)
        URANUS = (8.686e+25, 2.5559e7)
        NEPTUNE = (1.024e+26, 2.4746e7)

        def __init__(self, mass, radius):
            self.mass = mass      # in kilograms
            self.radius = radius  # in meters

        @property
        def surface_gravity(self):
            # universal gravitational constant  (m3 kg-1 s-2)
            G = 6.67300E-11
            return G * self.mass / (self.radius * self.radius)

    assert Planet.EARTH.value == (5.976e+24, 6378140.0)
    assert Planet.EARTH.surface_gravity == 9.802652743337129
    for name, const in Planet.__members__.items():
        assert name == const.name
        assert isinstance(const.surface_gravity, float)
