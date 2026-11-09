"""Entidad Categoria: agrupa productos (agregación 1..N con Producto)."""

from typing import TYPE_CHECKING

from entidades.base import Base
from entidades.validaciones import validar_texto

if TYPE_CHECKING:  # solo para los type hints; evita un import circular
    from entidades.producto import Producto


class Categoria(Base):
    """Categoría del catálogo. Agrega (no compone) a sus productos."""

    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.__nombre: str = validar_texto(nombre, "nombre")
        self.__descripcion: str = validar_texto(descripcion, "descripcion")
        self.__productos: list["Producto"] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = validar_texto(valor, "nombre")

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = validar_texto(valor, "descripcion")

    @property
    def productos(self) -> tuple["Producto", ...]:
        """Productos de la categoría (tupla: no se puede modificar desde afuera)."""
        return tuple(self.__productos)

    def contar_productos_activos(self) -> int:
        """Cantidad de productos de la categoría que no están eliminados."""
        return sum(1 for producto in self.__productos if not producto.eliminado)

    def _registrar_producto(self, producto: "Producto") -> None:
        """Uso interno: lo llama Producto al asignarse a esta categoría."""
        if producto not in self.__productos:
            self.__productos.append(producto)

    def _quitar_producto(self, producto: "Producto") -> None:
        """Uso interno: lo llama Producto al cambiar de categoría."""
        if producto in self.__productos:
            self.__productos.remove(producto)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - {self.descripcion}"
