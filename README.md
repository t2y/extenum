# extenum

[![Build Status](https://travis-ci.org/t2y/extenum.svg?branch=master)](https://travis-ci.org/t2y/extenum/)

Extended Enum classes for the Python 3 enum module.

The [enum](https://docs.python.org/3/library/enum.html) module was added
since 3.4. That's good enough for simple use.
The extenum is strongly inspired by Java Enum style described in
[Effective Java](http://en.wikipedia.org/wiki/Joshua_Bloch#Effective_Java)
and privides additional feature.


## How to install

NOTE: extenum supports Python 3 only.

    $ pip install extenum


## ConstantSpecificEnum

*ConstantSpecificEnum* class is inherited the standard Enum class and
provides the feature of constant specific method and function overloading
for Enum members.

Read [Effective Java](http://en.wikipedia.org/wiki/Joshua_Bloch#Effective_Java)
for more detail.


### Constant specific method implementation

Let's try to create Enum class with *ConstantSpecificEnum*.
To use method as function overloading, create the registory
with *RegisterFactory* for target Enum class.

```python
>>> from extenum import ConstantSpecificEnum, RegisterFactory
>>> class Operation(ConstantSpecificEnum):
...     PLUS = '+'
...     MINUS = '-'
...     TIMES = '*'
...     DIVIDE = '/'
...
...     overload = RegisterFactory()
...
...     @overload.register(PLUS)
...     def apply(self, x, y):
...         return x + y
...
...     @overload.register(MINUS)
...     def apply(self, x, y):
...         return x - y
...
...     @overload.register(TIMES)
...     def apply(self, x, y):
...         return x * y
...
...     @overload.register(DIVIDE)
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
>>> from extenum import ConstantSpecificEnum, RegisterFactory
>>> class PayrollDay(ConstantSpecificEnum):
...
...     class PayType(ConstantSpecificEnum):
...         WEEKDAY = 1
...         WEEKEND = 2
...
...         overload = RegisterFactory()
...
...         @overload.register(WEEKDAY)
...         def overtime_pay(self, hours, pay_rate):
...             return 0 if hours <= 8 else (hours - 8) * pay_rate / 2
...
...         @overload.register(WEEKEND)
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
...     overload = RegisterFactory()
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
