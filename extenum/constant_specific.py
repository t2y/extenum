from collections import defaultdict
from enum import Enum, EnumMeta, _EnumDict
from functools import update_wrapper

__all__ = [
    'ConstantSpecificEnum',
]

_OVERLOAD_FACTORY_NAME = 'overload'


class _MethodRegister:

    def __init__(self):
        self.cache = {}

    def __call__(self, constant):
        def register(func):
            def _register(*args, **kwargs):
                const = self.cache.get(args[0]._value_)
                if const is None:
                    raise ValueError('%r is not found in cache' % args[0])
                const_func = const.get(func.__name__)
                if const_func is None:
                    raise ValueError('%r.%s function is not found in cache' % (
                        args[0], func.__name__))
                return const_func(*args, **kwargs)

            self.cache[constant][func.__name__] = func
            update_wrapper(_register, func)
            return _register

        self.cache.setdefault(constant, {})
        return register


class _EnumDefaultDict(_EnumDict, defaultdict):

    def __missing__(self, key):
        if key == _OVERLOAD_FACTORY_NAME:
            self[key] = overlaod = _MethodRegister()
            return overlaod
        elif key == 'ConstantSpecificEnum':
            return ConstantSpecificEnum

        raise KeyError('Do not handle in here')


class _ConstantSpecificMeta(EnumMeta):

    @classmethod
    def __prepare__(metacls, cls, bases):
        return _EnumDefaultDict()

    def __new__(metacls, cls, bases, classdict):
        method_register = None
        overload_items = list(filter(
            lambda t: isinstance(t[1], _MethodRegister), classdict.items()))

        if overload_items:
            name, _ = overload_items[0]
            method_register = classdict.pop(name)
            classdict._member_names.pop(classdict._member_names.index(name))

        enum_class = super().__new__(metacls, cls, bases, classdict)

        if method_register is not None:
            enum_class._method_register = method_register

        wrapped_methods = {key for key, value in classdict.items()
                           if hasattr(value, '__wrapped__')}
        if wrapped_methods:
            metacls._validate_method_is_registered(enum_class, wrapped_methods)

        return enum_class

    @staticmethod
    def _validate_method_is_registered(enum_class, wrapped_methods):
        def validate(wrapped_methods, method_register):
            register_const = method_register.cache.get(const.value)
            if register_const is None:
                raise ValueError('%r is not registered' % const)
            register_methods = register_const.keys()
            for name in wrapped_methods:
                if name not in register_methods:
                    raise ValueError('%r.%s function is not registered' % (
                            const, name))

        for _, const in enum_class.__members__.items():
            method_register = getattr(enum_class, '_method_register', None)
            if method_register is not None:
                validate(wrapped_methods, method_register)


class ConstantSpecificEnum(Enum, metaclass=_ConstantSpecificMeta):
    pass
