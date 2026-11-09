"""Interfaz Calculable: comportamiento común de los objetos que tienen un total."""

from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz con un único método abstracto; no tiene atributos.

    Toda clase que la implemente debe saber actualizar su propio total.
    """

    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto que implementa la interfaz."""
        ...
