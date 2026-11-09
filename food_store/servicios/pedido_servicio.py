"""Servicio de pedidos: crea pedidos y mantiene coherente el stock."""

from entidades import Pedido
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import (
    DatoInvalidoError, EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class PedidoServicio:
    def __init__(self, usuario_servicio: UsuarioServicio, producto_servicio: ProductoServicio) -> None:
        self.__pedidos: list[Pedido] = []
        self.__usuario_servicio = usuario_servicio
        self.__producto_servicio = producto_servicio

    def listar(self) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario_id: int) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario.id == usuario_id]

    def buscar_por_id(self, pedido_id: int) -> Pedido:
        for pedido in self.listar():
            if pedido.id == pedido_id:
                return pedido
        raise EntidadNoEncontradaError(f"No existe el pedido con id {pedido_id}")

    def buscar_de_usuario(self, pedido_id: int, usuario: Usuario) -> Pedido:
        """Un pedido ajeno se informa como inexistente."""
        pedido = self.buscar_por_id(pedido_id)
        if pedido.usuario != usuario:
            raise EntidadNoEncontradaError(f"No existe el pedido con id {pedido_id}")
        return pedido

    # ----- creación en tres pasos: el pedido recién existe al confirmar --------
    def iniciar_pedido(self, usuario_id: int, forma_pago: FormaPago) -> Pedido:
        """Crea un pedido PENDIENTE todavía fuera de la colección (borrador)."""
        usuario = self.__usuario_servicio.buscar_por_id(usuario_id)
        return Pedido(usuario, forma_pago)

    def agregar_item(self, pedido: Pedido, producto_id: int, cantidad: int) -> None:
        producto = self.__producto_servicio.buscar_por_id(producto_id)
        pedido.agregar_detalle(cantidad, producto)

    def confirmar_creacion(self, pedido: Pedido) -> Pedido:
        """Calcula el total, descuenta el stock y recién entonces guarda el pedido."""
        if not pedido.detalles:
            raise DatoInvalidoError("El pedido debe tener al menos un detalle")
        for detalle in pedido.detalles:  # revalida todo antes de tocar nada
            if detalle.cantidad > detalle.producto.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente para '{detalle.producto.nombre}': "
                    f"solicitado {detalle.cantidad}, disponible {detalle.producto.stock}"
                )
        pedido.calcular_total()
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self.__pedidos.append(pedido)
        return pedido

    def crear(self, usuario_id: int, forma_pago: FormaPago, items: list[tuple[int, int]]) -> Pedido:
        """Atajo: crea un pedido completo; si algo falla no queda nada guardado."""
        pedido = self.iniciar_pedido(usuario_id, forma_pago)
        for producto_id, cantidad in items:
            self.agregar_item(pedido, producto_id, cantidad)
        return self.confirmar_creacion(pedido)

    # ----- cambios de estado / baja --------------------------------------------
    def __devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad

    def actualizar(
        self, pedido_id: int, estado: Estado | None = None, forma_pago: FormaPago | None = None
    ) -> Pedido:
        """Cambia estado y/o forma de pago; si algo no es válido no cambia nada."""
        pedido = self.buscar_por_id(pedido_id)
        if estado is not None and not pedido.estado.puede_pasar_a(estado):
            raise OperacionNoPermitidaError(
                f"Transición de estado inválida: {pedido.estado.name} -> {estado.name}"
            )
        if forma_pago is not None:
            pedido.forma_pago = forma_pago  # lanza si el pedido ya es final
        if estado is not None:
            pedido.estado = estado
        if estado is Estado.CANCELADO:
            self.__devolver_stock(pedido)
        return pedido

    def eliminar(self, pedido_id: int) -> None:
        """Baja lógica del pedido y sus detalles; devuelve stock si no estaba terminado/cancelado."""
        pedido = self.buscar_por_id(pedido_id)
        if not pedido.estado.es_final:
            self.__devolver_stock(pedido)
        pedido.eliminar()
