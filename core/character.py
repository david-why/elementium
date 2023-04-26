from typing import Any, Dict, List, Tuple, Type

from core.const import ElementRef
from core.element import Element, Types
from core.registry import Registry, registry
from core.variable import Variable

__all__ = ['Character']


class Character:
    """
    A `Character` in Elementium is simply a collection of `Element`s and all
    registered `Variable`s. The values for those `Variable`s are calculated
    based on the list of `Element`s.
    """

    def __init__(
        self, elements: List[ElementRef], registry: Registry = registry
    ) -> None:
        """
        Create a `Character` object.
        :param elements: The elements of this character. These are not
        necessatily unique; for example, the "Spell Slot" element may be added
        more than once for multiple spell slots.
        :param registry: The registry to use. Defaults to the global registry.
        """
        self.elements: Dict[int, List[Element]] = {}
        """The elements of this character, grouped by Element type"""
        for cls in elements:
            if isinstance(cls, tuple):
                cls = registry.get(*cls)
            self.elements.setdefault(cls.type, []).append(cls(self))
        self.elements[Types.VARIABLE] = []
        self._registry = registry
        for cls in registry[Types.VARIABLE].values():
            assert issubclass(cls, Variable) and cls.type == Types.VARIABLE
            self.elements[Types.VARIABLE].append(cls(self))

    @property
    def variables(self) -> Dict[str, Variable]:
        """The variables of this character."""
        variables = {}
        for var in self.elements[Types.VARIABLE]:
            variables[var.id] = var
        return variables

    @property
    def calculated_variables(self) -> Dict[str, Any]:
        """Shortcut for calling every variable."""
        return {k: v() for k, v in self.variables.items()}

    def get_variable(self, id: str):
        """
        Calculates a variable of the given id.
        :param id: The id of the variable.
        :return: The calculated result.
        :raise: DependencyError if variables have loop dependency.
        """
        return self.variables[id]()

    def get_elements_by_type(self, type: int) -> List[Element]:
        """
        Finds all elements of the given type.
        :param type: The type of elements to find.
        :return: All elements of the type specified in this character.
        """
        return self.elements.get(type, [])

    def count_elements(self, element: ElementRef) -> int:
        """
        Returns the number of occurrences of the `Element` in this character.
        :param element: The element to count.
        :return: The count of the given `Element` in this Character.
        """
        element = element if isinstance(element, type) else self._registry.get(*element)
        return sum(element.id == x.id for x in self.get_elements_by_type(element.type))
