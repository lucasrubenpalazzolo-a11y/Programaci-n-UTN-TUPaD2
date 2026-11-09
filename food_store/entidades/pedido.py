"""Entidad Pedido: compra de un usuario (composición 1..N con DetallePedido)."""

from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from entidades.validaciones import validar_cantidad
from enums import Estado, FormaPago
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)


class Pedido(Base, Calculable):
    """Pedido de un usuario. Es el único que crea y destruye sus DetallePedido."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if not isinstance(usuario, Usuario):
            raise DatoInvalidoError("No se puede crear un pedido sin usuario")
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario eliminado")
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__forma_pago: FormaPago = self.__validar_forma_pago(forma_pago)
        self.__detalles: list[DetallePedido] = []

    @staticmethod
    def __validar_forma_pago(valor: object) -> FormaPago:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago debe ser TARJETA, TRANSFERENCIA o EFECTIVO")
        return valor

    # ----- propiedades -------------------------------------------------
    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def total(self) -> float:
        return self.__total

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, nuevo: Estado) -> None:
        """Solo permite las transiciones válidas; si no, lanza y no cambia nada."""
        if not isinstance(nuevo, Estado):
            raise DatoInvalidoError("El estado no es válido")
        if not self.__estado.puede_pasar_a(nuevo):
            raise OperacionNoPermitidaError(
                f"Transición de estado inválida: {self.__estado.name} -> {nuevo.name}"
            )
        self.__estado = nuevo

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if self.__estado.es_final:
            raise OperacionNoPermitidaError(
                f"Un pedido {self.__estado.name} no admite más cambios"
            )
        self.__forma_pago = self.__validar_forma_pago(valor)

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        """Tupla: la lista interna no se puede modificar desde afuera."""
        return tuple(self.__detalles)

    # ----- métodos de negocio (firmas exigidas por la consigna) ----------
    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        """Agrega un detalle; si el producto ya estaba, suma la cantidad al existente.

        El precio sale del propio producto. Valida cantidad > 0, que el producto
        esté disponible y que la cantidad total no supere su stock.
        """
        self.__exigir_pendiente()
        if not isinstance(producto, Producto):
            raise DatoInvalidoError("El detalle debe referirse a un producto")
        if producto.eliminado or not producto.disponible:
            raise OperacionNoPermitidaError(f"El producto '{producto.nombre}' no está disponible")
        existente = self.buscar_detalle_por_producto(producto)
        cantidad_total = (existente.cantidad if existente else 0) + validar_cantidad(cantidad)
        if cantidad_total > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}': "
                f"solicitado {cantidad_total}, disponible {producto.stock}"
            )
        if existente is not None:
            existente.aumentar_cantidad(cantidad)
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        """Devuelve el detalle de ese producto o None si el pedido no lo incluye."""
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        """Quita el detalle del producto (el detalle muere con la composición)."""
        self.__exigir_pendiente()
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(
                f"El pedido no tiene un detalle del producto '{producto.nombre}'"
            )
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        """Implementa Calculable: el total es la suma de los subtotales de los detalles."""
        self.__total = round(sum(detalle.subtotal for detalle in self.__detalles), 2)

    # ----- baja lógica con cascada ---------------------------------------
    def eliminar(self) -> None:
        """Baja lógica del pedido y de todos sus detalles (polimorfismo sobre Base)."""
        super().eliminar()
        for detalle in self.__detalles:
            detalle.eliminar()

    # ----- internos --------------------------------------------------------
    def __exigir_pendiente(self) -> None:
        if self.__estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se pueden modificar los detalles de un pedido PENDIENTE "
                f"(estado actual: {self.__estado.name})"
            )

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.usuario.nombre_completo} | {self.estado.name} "
            f"| {self.forma_pago.name} | total: ${self.total:.2f} "
            f"| {self.fecha.strftime('%d/%m/%Y')}"
        )
