"""Utilidades compartidas por los servicios."""

from entidades import Base
from excepciones import FoodStoreError


def aplicar_cambios(entidad: Base, cambios: dict[str, object]) -> None:
    """Asigna varios atributos "todo o nada": si uno falla, restaura los anteriores."""
    anteriores = {nombre: getattr(entidad, nombre) for nombre in cambios}
    try:
        for nombre, valor in cambios.items():
            setattr(entidad, nombre, valor)
    except FoodStoreError:
        for nombre, valor in anteriores.items():
            setattr(entidad, nombre, valor)
        raise
