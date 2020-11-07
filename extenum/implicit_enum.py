import builtins
from collections import defaultdict
from enum import Enum, EnumMeta, _EnumDict
from itertools import count

__all__ = [
    'ImplicitEnum',
]


class _EnumDefaultDict(_EnumDict, defaultdict):

    def __init__(self, start=1):
        super().__init__()
        self._implicit_const_counter = count(start)

    def __missing__(self, key):
        if key.startswith('__') or getattr(builtins, key, None) is not None:
            raise KeyError('Not constant member')

        member_values = {self[const] for const in self._member_names}
        value = next(self._implicit_const_counter)
        while value in member_values:
            value = next(self._implicit_const_counter)
        self[key] = value


class _ImplicitEnumMeta(EnumMeta):

    @classmethod
    def __prepare__(metacls, cls, bases):
        return _EnumDefaultDict()


class ImplicitEnum(Enum, metaclass=_ImplicitEnumMeta):
    pass
