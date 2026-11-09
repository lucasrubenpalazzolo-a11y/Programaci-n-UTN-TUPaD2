"""Enumerado Estado: ciclo de vida de un pedido y sus transiciones válidas."""

from enum import Enum


class Estado(Enum):
    """Estado de un pedido.

    Transiciones válidas:
        PENDIENTE  -> CONFIRMADO | CANCELADO
        CONFIRMADO -> TERMINADO  | CANCELADO
        TERMINADO y CANCELADO son estados finales (no cambian más).
    """

    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"

    def transiciones_validas(self) -> frozenset["Estado"]:
        """Devuelve los estados a los que se puede pasar desde este estado."""
        permitidas: dict[Estado, frozenset[Estado]] = {
            Estado.PENDIENTE: frozenset({Estado.CONFIRMADO, Estado.CANCELADO}),
            Estado.CONFIRMADO: frozenset({Estado.TERMINADO, Estado.CANCELADO}),
            Estado.TERMINADO: frozenset(),
            Estado.CANCELADO: frozenset(),
        }
        return permitidas[self]

    def puede_pasar_a(self, destino: "Estado") -> bool:
        """Indica si la transición desde este estado hacia `destino` es válida."""
        return destino in self.transiciones_validas()

    @property
    def es_final(self) -> bool:
        """True si el pedido ya no admite más cambios (TERMINADO o CANCELADO)."""
        return not self.transiciones_validas()
