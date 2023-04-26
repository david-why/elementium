from operator import add, floordiv, mul, sub, truediv
from typing import TYPE_CHECKING, Callable, Generic, TypeVar, Union, cast, Type

from core.const import (
    ElementRef,
    SupportsAdd,
    SupportsFloorDiv,
    SupportsMul,
    SupportsRAdd,
    SupportsRFloorDiv,
    SupportsRMul,
    SupportsRSub,
    SupportsRTrueDiv,
    SupportsSub,
    SupportsTrueDiv,
    SupportsBool,
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from core.character import Character

__all__ = ['Formula']

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


class Formula(Generic[T]):
    """
    A `Formula` tells Elementium how to calculate a `Variable`. It may be
    based on `Elements` of a character and any other `Variable`s. When called,
    a `Formula` object will call its `function` and return the value.

    Example usage:

    ```python
    from core.formula import Formula as F
    from core.registry import registry
    wizard_level = F.count((2, 'wizard'))
    wizard_hp = F.has((2, 'wizard')) * 2 + F.count((2, 'wizard')) * 4
    ```
    """

    __slots__ = ('function',)

    def __init__(self, function: Callable[['Character'], T]) -> None:
        """
        Create a `Formula` object from a callable.
        :param function: The callable that generates a value for this
        `Variable` given the character.
        """
        self.function = function

    def __call__(self, character: 'Character') -> T:
        return self.function(character)

    @classmethod
    def const(cls, value: T) -> 'Self':
        """
        Create a `Formula` object that returns the constant value.
        :param value: The constant formula value.
        :return: A `Formula` object that always evaluates to the value.
        """
        return cls(lambda character: value)

    @classmethod
    def var(cls, name: str) -> 'Self':
        """
        Create a `Formula` object that returns a variable value.
        :param value: The constant formula value.
        :return: A `Formula` object that always evaluates to the value.
        """
        return cls(lambda character: character.get_variable(name))

    @classmethod
    def count(cls, element: ElementRef) -> 'Formula[int]':
        """
        Create a `Formula` object that returns the count of an element.
        :param element: The element to count.
        :return: A `Formula` object that evaluates to the count of the element
        in the character.
        """
        return cast(Type[Formula[int]], cls)(
            lambda character: character.count_elements(element)
        )

    @classmethod
    def has(cls, element: ElementRef) -> 'Formula[bool]':
        """
        Create a `Formula` object that returns whether the character has an
        element (i.e. count > 0).
        :param element: The element to find.
        :return: A `Formula` object that evaluates to `True` if the character
        has the element, `False` otherwise.
        """
        return cast(Type[Formula[bool]], cls)(
            lambda character: character.count_elements(element) > 0
        )

    @classmethod
    def if_(
        cls,
        expr: Callable[['Character'], SupportsBool],
        if_true: Callable[['Character'], T],
        if_false: Callable[['Character'], T],
    ) -> 'Self':
        """
        Create a `Formula` object that evaluates to `if_true` or `if_false`
        depending on if `expr` evaluates to True.
        :param expr: The boolean expression to evaluate.
        :param if_true: Return value if `expr` evaluates to `True`.
        :param if_false: Return value if `expr` evaluates to `False`.
        :return: A `Formula` object that evaluates according to above rules.
        """
        return cls(
            lambda character: (if_true if expr(character) else if_false)(character)
        )

    def _operator(
        self, operator: Callable[[T, U], V], value: Union[Callable[['Character'], U], U]
    ) -> 'Formula[V]':
        func = value if callable(value) else lambda character: value
        return Formula(
            lambda character: operator(self.function(character), func(character))
        )

    def __add__(
        self,
        func: Union[Callable[['Character'], SupportsRAdd[T, U]], SupportsRAdd[T, U]],
    ) -> 'Formula[U]':
        return self._operator(add, func)

    def __sub__(
        self,
        func: Union[Callable[['Character'], SupportsRSub[T, U]], SupportsRSub[T, U]],
    ) -> 'Formula[U]':
        return self._operator(sub, func)

    def __mul__(
        self,
        func: Union[Callable[['Character'], SupportsRMul[T, U]], SupportsRMul[T, U]],
    ) -> 'Formula[U]':
        return self._operator(mul, func)

    def __truediv__(
        self,
        func: Union[
            Callable[['Character'], SupportsRTrueDiv[T, U]], SupportsRTrueDiv[T, U]
        ],
    ) -> 'Formula[U]':
        return self._operator(truediv, func)

    def __floordiv__(
        self,
        func: Union[
            Callable[['Character'], SupportsRFloorDiv[T, U]], SupportsRFloorDiv[T, U]
        ],
    ) -> 'Formula[U]':
        return self._operator(floordiv, func)

    def _roperator(
        self, operator: Callable[[U, T], V], value: Union[Callable[['Character'], U], U]
    ) -> 'Formula[V]':
        func = value if callable(value) else lambda character: value
        return Formula(
            lambda character: operator(func(character), self.function(character))
        )

    def __radd__(
        self,
        func: Union[Callable[['Character'], SupportsAdd[T, U]], SupportsAdd[T, U]],
    ) -> 'Formula[U]':
        return self._roperator(add, func)

    def __rsub__(
        self, func: Union[Callable[['Character'], SupportsSub[T, U]], SupportsSub[T, U]]
    ) -> 'Formula[U]':
        return self._roperator(sub, func)

    def __rmul__(
        self, func: Union[Callable[['Character'], SupportsMul[T, U]], SupportsMul[T, U]]
    ) -> 'Formula[U]':
        return self._roperator(mul, func)

    def __rtruediv__(
        self,
        func: Union[
            Callable[['Character'], SupportsTrueDiv[T, U]], SupportsTrueDiv[T, U]
        ],
    ) -> 'Formula[U]':
        return self._roperator(truediv, func)

    def __rfloordiv__(
        self,
        func: Union[
            Callable[['Character'], SupportsFloorDiv[T, U]], SupportsFloorDiv[T, U]
        ],
    ) -> 'Formula[U]':
        return self._roperator(floordiv, func)
