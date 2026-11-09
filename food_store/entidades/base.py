"""Clase abstracta Base: superclase de todas las entidades del dominio."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, ClassVar


class Base(ABC):
    """Atributos y comportamiento comunes: id, baja lógica y fecha de creación.

    Decisión de diseño: cada subclase tiene su propio contador de ids
    (Categoria 1, 2, 3...; Producto 1, 2, 3...), lo que hace más cómodo elegir
    por id desde la consola. Por eso `__eq__` compara clase e id.
    """

    _siguiente_id: ClassVar[int] = 1

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Cada subclase concreta arranca su propio contador en 1."""
        super().__init_subclass__(**kwargs)
        cls._siguiente_id = 1

    def __init__(self) -> None:
        clase = type(self)
        self.__id: int = clase._siguiente_id
        clase._siguiente_id += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        """Identificador autogenerado; no se puede modificar."""
        return self.__id

    @property
    def eliminado(self) -> bool:
        """True si la entidad fue dada de baja (baja lógica)."""
        return self.__eliminado

    @property
    def creado_en(self) -> datetime:
        """Fecha y hora de creación, asignada en el constructor."""
        return self.__creado_en

    def eliminar(self) -> None:
        """Baja lógica: marca eliminado = True; el objeto sigue en la colección."""
        self.__eliminado = True

    def __eq__(self, otro: object) -> bool:
        """Dos entidades son iguales si son de la misma clase y tienen el mismo id."""
        if self is otro:
            return True
        if not isinstance(otro, Base):
            return NotImplemented
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        """Coherente con __eq__ (al definir __eq__ Python anula el hash heredado)."""
        return hash((type(self).__name__, self.__id))

    @abstractmethod
    def __str__(self) -> str:
        """Cada entidad debe describirse en una línea útil para los listados."""
        ...
