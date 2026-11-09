"""Entidad DetallePedido: línea de un pedido (producto + cantidad + subtotal)."""

from entidades.base import Base
from entidades.producto import Producto
from entidades.validaciones import validar_cantidad
from excepciones import DatoInvalidoError


class DetallePedido(Base):
    """Línea de pedido. Nace y muere con su Pedido (composición): solo Pedido la crea.

    El subtotal se calcula con el precio del producto en el momento de agregarlo,
    por lo que un cambio posterior de precio no altera pedidos ya armados.
    """

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if not isinstance(producto, Producto):
            raise DatoInvalidoError("El detalle debe referirse a un producto")
        self.__producto: Producto = producto
        self.__cantidad: int = validar_cantidad(cantidad)
        self.__subtotal: float = round(self.__cantidad * producto.precio, 2)

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def aumentar_cantidad(self, cantidad_extra: int) -> None:
        """Suma unidades al detalle (mismo producto agregado de nuevo al pedido)."""
        extra = validar_cantidad(cantidad_extra)
        self.__cantidad += extra
        self.__subtotal = round(self.__subtotal + extra * self.__producto.precio, 2)

    def __str__(self) -> str:
        return (
            f"{self.producto.nombre} | cantidad: {self.cantidad} "
            f"| subtotal: ${self.subtotal:.2f}"
        )
