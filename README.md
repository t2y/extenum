# extenum

[![Build Status](https://travis-ci.org/t2y/extenum.svg?branch=master)](https://travis-ci.org/t2y/extenum/)
[![Latest Version](https://img.shields.io/pypi/v/extenum.svg)](https://pypi.python.org/pypi/extenum/)
[![Downloads](https://img.shields.io/pypi/dm/extenum.svg)](https://pypi.python.org/pypi/extenum/)
[![License](https://img.shields.io/pypi/l/extenum.svg)](https://pypi.python.org/pypi/extenum/)


Extended Enum classes for Python 3 enum module.

The [enum](https://docs.python.org/3/library/enum.html) module was added
since 3.4. That's good enough for simple use.
The extenum is strongly inspired by Java Enum style described in
[Effective Java](http://en.wikipedia.org/wiki/Joshua_Bloch#Effective_Java)
and provides additional feature.


## How to install

```bash
$ pip install extenum
```

## ConstantSpecificEnum

*ConstantSpecificEnum* class is inherited the standard Enum class and
provides the feature of constant specific method and function overloading
for Enum members.

Read [Effective Java](http://en.wikipedia.org/wiki/Joshua_Bloch#Effective_Java)
for more detail.


### Constant specific method implementation

Let's try to create Enum class with *ConstantSpecificEnum*.
To use a method as function overloading, add *@overload(CONSTANT)* decorator
on that method. The *overload* decorator is implicitly defined as well as
you'll see later in *ImplicitEnum* section.

```python
>>> from extenum import ConstantSpecificEnum
>>> class Operation(ConstantSpecificEnum):
...     PLUS = '+'
...     MINUS = '-'
...     TIMES = '*'
...     DIVIDE = '/'
...
...     @overload(PLUS)
...     def apply(self, x, y):
...         return x + y
...
...     @overload(MINUS)
...     def apply(self, x, y):
...         return x - y
...
...     @overload(TIMES)
...     def apply(self, x, y):
...         return x * y
...
...     @overload(DIVIDE)
...     def apply(self, x, y):
...         return x / y
...
>>> for name, const in Operation.__members__.items():
...     print(name, ':', const.apply(2, 4))
...
PLUS : 6
MINUS : -2
TIMES : 8
DIVIDE : 0.5

```


### Strategy enum pattern

The strategy enum is more complex pattern based on constant specific method.

```python
>>> from extenum import ConstantSpecificEnum
>>> class PayrollDay(ConstantSpecificEnum):
...
...     class PayType(ConstantSpecificEnum):
...         WEEKDAY = 1
...         WEEKEND = 2
...
...         @overload(WEEKDAY)
...         def overtime_pay(self, hours, pay_rate):
...             return 0 if hours <= 8 else (hours - 8) * pay_rate / 2
...
...         @overload(WEEKEND)
...         def overtime_pay(self, hours, pay_rate):
...             return hours * pay_rate / 2
...
...         def pay(self, hours_worked, pay_rate):
...             base_pay = hours_worked * pay_rate
...             overtime_pay = self.overtime_pay(hours_worked, pay_rate)
...             return base_pay + overtime_pay
...
...     MONDAY = PayType.WEEKDAY
...     TUESDAY = PayType.WEEKDAY
...     WEDNESDAY = PayType.WEEKDAY
...     THURSDAY = PayType.WEEKDAY
...     FRIDAY = PayType.WEEKDAY
...     SATURDAY = PayType.WEEKEND
...     SUNDAY = PayType.WEEKEND
...
...     def pay(self, hours_worked, pay_rate):
...         return self.value.pay(hours_worked, pay_rate)
...
>>> PayrollDay.MONDAY.pay(10, 1000.0)
11000.0
>>> PayrollDay.WEDNESDAY.pay(8, 1000.0)
8000.0
>>> PayrollDay.SATURDAY.pay(10, 1000.0)
15000.0
>>> PayrollDay.SUNDAY.pay(8, 1000.0)
12000.0

```


## ImplicitEnum

Before describing what *ImplicitEnum* class is, read good article written by
Nick Coghlan as below.

* [Support for alternate declaration syntaxes](http://python-notes.curiousefficiency.org/en/latest/python3/enum_creation.html#support-for-alternate-declaration-syntaxes)

OK. I guess you've already understood why the standard enum module haven't
support implicit declaration syntax.

Put aside its needs for now, Nick indicates how to implement *ImplicitEnum*.
So, let's try to implement it experimentally using the special method,
`__missing__` in defaultdict and `__prepare__` in Metaclass.

```python
>>> from extenum import ImplicitEnum
>>> class Color(ImplicitEnum):
...     RED
...     GREEN
...     BLUE
...
>>> for name, const in Color.__members__.items():
...     print(name, ':', const.value)
...
RED : 1
GREEN : 2
BLUE : 3

```

It works well if some constants are explicit and the rest are implicit.

```python
>>> class Numbers(ImplicitEnum):
...     ONE = 1
...     TWO = 2
...     THREE
...
>>> Numbers.THREE.value
3

```

However, it depends on the declaration order.

```python
>>> class DuplicatedValues(ImplicitEnum):
...     ONE
...     TWO = 1
...     THREE = 1
...
>>> DuplicatedValues.ONE.value
1
>>> DuplicatedValues.TWO.value
1
>>> DuplicatedValues.THREE.value
1

```


## EnumSet

EnumSet is one of the specialized implementation of Set interface for enumeration type,
inspired by [Java EnumSet](http://docs.oracle.com/javase/8/docs/api/java/util/EnumSet.html).

It provides utility functions to handle multiple Enum constants.

```python
>>> from enum import Enum
>>> from extenum import EnumSet
>>> class Mode(Enum):
...     READ = 4
...     WRITE = 2
...     EXECUTE = 1
...
...     @classmethod
...     def set_of(cls, values):
...         opts = EnumSet.none_of(cls)
...         for value in values:
...             opts.add(cls(value))
...         return opts
...
>>> Mode.set_of([4, 2])  # doctest: +SKIP
EnumSet({<Mode.READ: 4>, <Mode.WRITE: 2>})
```

To create EnumSet with all Enum members:

```python
>>> EnumSet.all_of(Mode)  # doctest: +SKIP
EnumSet({<Mode.READ: 4>, <Mode.WRITE: 2>, <Mode.EXECUTE: 1>})
```

Or, to create EnumSet with arbitrary Enum members:

```python
>>> enumset = EnumSet.of(Mode.READ, Mode.EXECUTE)
>>> enumset  # doctest: +SKIP
EnumSet({<Mode.READ: 4>, <Mode.EXECUTE: 1>})
>>> enumset.update(EnumSet.of(Mode.READ, Mode.WRITE))
>>> enumset  # doctest: +SKIP
EnumSet({<Mode.READ: 4>, <Mode.WRITE: 2>, <Mode.EXECUTE: 1>})
```
