from typing import TYPE_CHECKING, List, Protocol, Tuple, Type, TypeVar, Union, Callable

if TYPE_CHECKING:
    from core.element import Element
    from core.variable import Variable

T = TypeVar('T', contravariant=True)
U = TypeVar('U', covariant=True)

ElementRef = Union[Type['Element'], Tuple[int, str]]
ElementMultiRef = Union[ElementRef, int, Tuple[int, Callable[[Type['Element']], bool]]]
OptionTuple = Tuple[List[ElementMultiRef], int]


class CircularDependencyError(TypeError):
    """Variable loop dependency error."""

    def __init__(self, variable: 'Variable') -> None:
        super().__init__(f'Variable {variable.name} trapped in circular dependency')
        self.variable = variable


class SpellFlags:
    VERBAL = 1 << 0
    SOMANTIC = 1 << 1
    MATERIAL = 1 << 2
    CONCENTRATION = 1 << 3
    RITUAL = 1 << 4
    SPECIAL = 1 << 5


class SpellSchool:
    Abjuration = 1
    Conjuration = 2
    Divination = 3
    Enchantment = 4
    Evocation = 5
    Illusion = 6
    Necromancy = 7
    Transmutation = 8


class TimeUnit:
    Instantaneous = 1
    Second = 2
    Round = 3
    Minute = 4
    Hour = 5
    Day = 6
    Month = 7
    Year = 8
    UntilDispelled = 9
    Action = 10
    BonusAction = 11
    Reaction = 12
    Special = 99


class DistanceUnit:
    Touch = 1
    Foot = 2
    Mile = 3
    Special = 99


class Time:
    def __init__(self, number: float, unit: int) -> None:
        self.number = number
        self.unit = unit


class Distance:
    def __init__(self, number: float, unit: int) -> None:
        self.number = number
        self.unit = unit


class SupportsBool(Protocol):
    def __bool__(self) -> bool:
        ...


class SupportsAdd(Protocol[T, U]):
    def __add__(self, value: T, /) -> U:
        ...


class SupportsSub(Protocol[T, U]):
    def __sub__(self, value: T, /) -> U:
        ...


class SupportsMul(Protocol[T, U]):
    def __add__(self, value: T, /) -> U:
        ...


class SupportsTrueDiv(Protocol[T, U]):
    def __truediv__(self, value: T, /) -> U:
        ...


class SupportsFloorDiv(Protocol[T, U]):
    def __floordiv__(self, value: T, /) -> U:
        ...


class SupportsRAdd(Protocol[T, U]):
    def __radd__(self, value: T, /) -> U:
        ...


class SupportsRSub(Protocol[T, U]):
    def __rsub__(self, value: T, /) -> U:
        ...


class SupportsRMul(Protocol[T, U]):
    def __radd__(self, value: T, /) -> U:
        ...


class SupportsRTrueDiv(Protocol[T, U]):
    def __rtruediv__(self, value: T, /) -> U:
        ...


class SupportsRFloorDiv(Protocol[T, U]):
    def __rfloordiv__(self, value: T, /) -> U:
        ...
