from operator import methodcaller

import pytest
from extenum import ConstantSpecificEnum


def test_constant_specific_method():
    class TestEnum(ConstantSpecificEnum):
        ONE = 1
        TWO = 2

        @property
        @overload(ONE)
        def alias(self):
            return 'alias {}'.format(self.name)

        @property
        @overload(TWO)
        def alias(self):
            return 'alias {}'.format(self.name)

        @overload(ONE)
        def is_one(self):
            return True

        @overload(ONE)
        def is_two(self):
            return False

        @overload(TWO)
        def is_one(self):
            return False

        @overload(TWO)
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


def test_strategy_enum_pattern():
    class PayrollDay(ConstantSpecificEnum):

        class PayType(ConstantSpecificEnum):
            WEEKDAY = 1
            WEEKEND = 2

            @overload(WEEKDAY)
            def overtime_pay(self, hours, pay_rate):
                return 0 if hours <= 8 else (hours - 8) * pay_rate / 2

            @overload(WEEKEND)
            def overtime_pay(self, hours, pay_rate):
                return hours * pay_rate / 2

            def pay(self, hours_worked, pay_rate):
                base_pay = hours_worked * pay_rate
                overtime_pay = self.overtime_pay(hours_worked, pay_rate)
                return base_pay + overtime_pay

        MONDAY = PayType.WEEKDAY
        TUESDAY = PayType.WEEKDAY
        WEDNESDAY = PayType.WEEKDAY
        THURSDAY = PayType.WEEKDAY
        FRIDAY = PayType.WEEKDAY
        SATURDAY = PayType.WEEKEND
        SUNDAY = PayType.WEEKEND

        def pay(self, hours_worked, pay_rate):
            return self.value.pay(hours_worked, pay_rate)

    weekday = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
    weekend = ['SATURDAY', 'SUNDAY']
    for name, const in PayrollDay.__members__.items():
        if name in weekday:
            assert const.pay(8, 1000.0) == 8000.0
        elif name in weekend:
            assert const.pay(8, 1000.0) == 12000.0
        else:  # should be PayType
            assert const._value_.WEEKDAY.overtime_pay(10, 100.0) == 100.0
            assert const._value_.WEEKEND.overtime_pay(10, 100.0) == 500.0


def test_raise_const_is_not_registered():
    with pytest.raises(ValueError) as excinfo:
        class TestEnum(ConstantSpecificEnum):
            ONE = 1
            TWO = 2

            @overload(ONE)
            def test(self):
                pass

    expected = '<TestEnum.TWO: 2> is not registered'
    assert str(excinfo.value) == expected


def test_raise_const_is_not_defined():
    with pytest.raises(NameError) as excinfo:
        class TestEnum(ConstantSpecificEnum):
            ONE = 1

            @overload(ONE)
            def one(self):
                pass

            @overload(TWO)
            def one(self):
                pass

    expected = "name 'TWO' is not defined"
    assert str(excinfo.value) == expected


def test_raise_function_is_not_registered():
    with pytest.raises(ValueError) as excinfo:
        class TestEnum(ConstantSpecificEnum):
            ONE = 1
            TWO = 2

            @overload(ONE)
            def one(self):
                pass

            @overload(TWO)
            def one(self):
                pass

            @overload(TWO)
            def two(self):
                pass

    expected = '<TestEnum.ONE: 1>.two function is not registered'
    assert str(excinfo.value) == expected


def test_work_as_planet_constant_specific_enum():
    class Planet(ConstantSpecificEnum):
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

        @overload(MERCURY)
        def name(self):
            return 'MERCURY'

        @overload(VENUS)
        def name(self):
            return 'VENUS'

        @overload(EARTH)
        def name(self):
            return 'EARTH'

        @overload(MARS)
        def name(self):
            return 'MARS'

        @overload(JUPITER)
        def name(self):
            return 'JUPITER'

        @overload(SATURN)
        def name(self):
            return 'SATURN'

        @overload(URANUS)
        def name(self):
            return 'URANUS'

        @overload(NEPTUNE)
        def name(self):
            return 'NEPTUNE'

    assert Planet.EARTH.value == (5.976e+24, 6378140.0)
    assert Planet.EARTH.surface_gravity == 9.802652743337129
    for name, const in Planet.__members__.items():
        assert name == const.name()
