from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    TypeVar,
    Union,
    Callable,
    ClassVar,
)

from core.const import CircularDependencyError, ElementRef, OptionTuple
from core.element import Element, Types
from core.registry import Registry

if TYPE_CHECKING:
    from core.character import Character

__all__ = ['Variable']

T = TypeVar('T')


class Variable(Element, _check=False, register=False):
    """
    In the context of Elementium, a `Variable` is any changing attribute of a
    character. For example, the Strength score, the initiative bonus, the
    number of Level 1 spell slots, the level, etc. are all Variables.

    `Variable` is a subclass of `Element`, because a `Variable` is also an
    attribute of a character.

    Each `Variable` *subclass* defines one such variable. Each variable must
    have a `formula`, which defines how the Variable is calculated. See the
    docstring for `Formula` for more information.
    """

    type = Types.VARIABLE

    formula: ClassVar[Callable[['Character'], Any]]

    def __init__(self, character: 'Character'):
        super().__init__(character)
        self._lock = False

    def __init_subclass__(
        cls,
        *,
        formula: Optional[Callable[['Character'], Any]] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        granted: Optional[List[ElementRef]] = None,
        options: Optional[List[OptionTuple]] = None,
        register: Union[Registry, bool] = True,
        _check: bool = True,
    ) -> None:
        if formula is not None:
            cls.formula = formula
        for attr in ['formula']:
            if not hasattr(cls, attr):
                name = cls.__qualname__
                raise TypeError(f'Variable subclass {name} has no attribute {attr}')
        return super().__init_subclass__(
            id=id,
            name=name,
            description=description,
            granted=granted,
            options=options,
            register=register,
            _check=_check,
        )

    def __call__(self) -> Any:
        if self._lock:
            raise CircularDependencyError(self)
        self._lock = True
        value = type(self).formula(self.character)
        self._lock = False
        return value
