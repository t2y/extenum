from enum import Enum
from operator import le


__all__ = [
    'EnumSet',
]


class EnumTypeMode(Enum):
    NONE = 1
    ALL = 2


class EnumSetMeta(type):

    def none_of(cls, enum_type):
        return cls._create_enum_set(enum_type, EnumTypeMode.NONE)

    def all_of(cls, enum_type):
        return cls._create_enum_set(enum_type, EnumTypeMode.ALL)

    def of(cls, *constants):
        enum_type = cls._get_enum_type(constants)
        enumset = cls._create_enum_set(enum_type, EnumTypeMode.NONE)
        enumset.update(constants)
        return enumset

    def range(cls, from_, to):
        def get_condition_function(from_, to):
            try:
                le(from_, to)
            except TypeError:
                return lambda fr, c, to: fr.value <= c.value <= to.value
            else:
                return lambda fr, c, to: fr <= c <= to

        enum_type = cls._get_enum_type((from_, to))
        enumset = cls._create_enum_set(enum_type, EnumTypeMode.NONE)
        cond = get_condition_function(from_, to)
        range_set = {const for const in enum_type if cond(from_, const, to)}
        enumset.update(range_set)
        return enumset

    def _create_enum_set(cls, enum_type, mode):
        enumset = cls.__new__(cls, enum_type)
        if mode is EnumTypeMode.ALL:
            enumset.update(enum_type)
        return enumset

    def _get_enum_type(cls, constants):
        s = {const.__class__ for const in constants}
        if len(s) != 1:
            raise ValueError('%r are not consistent Enum type' % (constants,))
        return s.pop()


class EnumSet(set, metaclass=EnumSetMeta):

    def __new__(cls, enum_type):
        if not issubclass(enum_type, Enum):
            raise TypeError('%r is not Enum subclass' % enum_type)

        enumset = super().__new__(cls)
        enumset._enum_type = enum_type
        return enumset

    def __init__(self, enum_type):
        super().__init__(self)

    def add(self, elem):
        self._validate(elem)
        super().add(elem)

    def update(self, *others):
        for other in others:
            for elem in other:
                self.add(elem)

    def _validate(self, elem):
        if not isinstance(elem, self._enum_type):
            msg = '%r is not member of %r' % (elem, self._enum_type)
            raise ValueError(msg)
