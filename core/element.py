import inspect
from typing import TYPE_CHECKING, ClassVar, List, Optional, Tuple, Type, Union, Set

from core.const import ElementRef, OptionTuple
from core.registry import Registry, registry

if TYPE_CHECKING:
    from character import Character

__all__ = ['Element', 'Types']


class Types:
    VARIABLE = 0
    ABILITY = 10
    SPELL = 20
    ACTION = 30
    FEAT = 40
    ITEM = 45
    TRAIT = 50
    RACE = 60
    FEATURE = 70
    CLASS = 80
    BASE = 90


class Element:
    """
    This is where the magic happens.

    Each `Element` *subclass* is a single feature/trait/selection. For
    example, the Wizard class, the School of Abjuration subclass, the
    Spellcasting feature, the Mage Hand spell, the Gnome race, Ability Score
    Increase, etc. are all subclasses of `Element`.
    """

    type: ClassVar[int]
    id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str] = 'N/A'
    granted: ClassVar[List[ElementRef]] = []
    options: ClassVar[List[OptionTuple]] = []

    _registry: ClassVar[Registry]

    @classmethod
    def _infer_type(cls):
        """
        Guesses the Element type based on the module. Basically checks the
        "default_type" attribute on the module object.
        """
        module = inspect.getmodule(cls)
        if module is None or not hasattr(module, 'default_type'):
            return
        cls.type = module.default_type

    def __init__(self, character: 'Character'):
        self.character = character

    def __init_subclass__(
        cls,
        *,
        type: Optional[int] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        granted: Optional[List[ElementRef]] = None,
        options: Optional[List[OptionTuple]] = None,
        register: Union[Registry, bool] = True,
        _check: bool = True,
    ) -> None:
        if type is not None:
            cls.type = type
        if not hasattr(cls, 'type'):
            cls._infer_type()
        if id is not None:
            cls.id = id
        if name is not None:
            cls.name = name
        if description is not None:
            cls.description = description
        if granted is not None:
            cls.granted = granted
        if options is not None:
            cls.options = options
        for attr in ['type', 'id', 'name']:
            if not hasattr(cls, attr) and _check:
                name = cls.__qualname__
                raise TypeError(f'Element subclass {name} has no attribute {attr}')
        cls._registry = register if isinstance(register, Registry) else registry
        if register is not False:
            register = registry if register is True else register
            register.register(cls)

    def get_choices(self, option: int) -> Set[Type['Element']]:
        choices, _ = self.options[option]
        res: Set[Type['Element']] = set()
        for choice in choices:
            if isinstance(choice, type):  # Type[Element]
                res.add(choice)
            elif isinstance(choice, tuple):
                typ, spec = choice
                if callable(spec):  # Tuple[int, Callable[[Type['Element']], bool]]
                    for item in self._registry[typ].values():
                        if spec(item):
                            res.add(item)
                else:  # Tuple[int, str]
                    res.add(self._registry.get(typ, spec))
            else:  # int
                res.update(self._registry[choice].values())
        return res
