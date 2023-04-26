from typing import TYPE_CHECKING, Dict, Type, TypeVar

if TYPE_CHECKING:
    from core.element import Element

__all__ = ['Registry', 'registry']

T = TypeVar('T', object, None)  # workaround for vscode type checker

_Element = None  # preventing circular import from core.element


class Registry:
    def __init__(self) -> None:
        self.registry: Dict[int, Dict[str, Type['Element']]] = {}

    def register(self, cls: Type['Element']) -> None:
        global _Element
        if _Element is None:
            from core.element import Element as _Element
        if cls is _Element:
            raise TypeError('Cannot register base class Element')
        registry = self.registry.setdefault(cls.type, {})
        if cls.id in registry:
            raise ValueError(f'Class {cls.__qualname__} registered twice')
        registry[cls.id] = cls

    def get(self, type: int, id: str) -> Type['Element']:
        return self.registry[type][id]

    def __getitem__(self, type: int) -> Dict[str, Type['Element']]:
        return self.registry.get(type, {})


registry = Registry()
