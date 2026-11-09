"""Enumerado FormaPago: medios de pago admitidos por un pedido."""

from enum import Enum


class FormaPago(Enum):
    """Forma de pago de un pedido."""

    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"
    EFECTIVO = "Efectivo"
