"""Entidad Producto: artículo del catálogo (N..1 con Categoria)."""

from entidades.base import Base
from entidades.categoria import Categoria
from entidades.validaciones import (
    validar_booleano,
    validar_precio,
    validar_stock,
    validar_texto,
    validar_texto_opcional,
)
from excepciones import DatoInvalidoError


class Producto(Base):
    """Producto con precio, stock y disponibilidad; pertenece a una Categoria."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
        descripcion: str = "",
        imagen: str = "",
        disponible: bool = True,
    ) -> None:
        super().__init__()
        self.__nombre: str = validar_texto(nombre, "nombre")
        self.__precio: float = validar_precio(precio)
        self.__stock: int = validar_stock(stock)
        self.__descripcion: str = validar_texto_opcional(descripcion, "descripcion")
        self.__imagen: str = validar_texto_opcional(imagen, "imagen")
        self.__disponible: bool = validar_booleano(disponible, "disponible")
        self.__categoria: Categoria = self.__validar_categoria(categoria)
        self.__categoria._registrar_producto(self)

    @staticmethod
    def __validar_categoria(valor: object) -> Categoria:
        if not isinstance(valor, Categoria):
            raise DatoInvalidoError("El producto debe pertenecer a una categoría")
        return valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = validar_texto(valor, "nombre")

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        self.__precio = validar_precio(valor)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = validar_texto_opcional(valor, "descripcion")

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        self.__stock = validar_stock(valor)

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = validar_texto_opcional(valor, "imagen")

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = validar_booleano(valor, "disponible")

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        """Cambia de categoría manteniendo coherentes ambos lados de la relación."""
        nueva = self.__validar_categoria(valor)
        self.__categoria._quitar_producto(self)
        nueva._registrar_producto(self)
        self.__categoria = nueva

    def __str__(self) -> str:
        estado = "disponible" if self.disponible else "NO disponible"
        return (
            f"[{self.id}] {self.nombre} | ${self.precio:.2f} | stock: {self.stock} "
            f"| {self.categoria.nombre} | {estado}"
        )
