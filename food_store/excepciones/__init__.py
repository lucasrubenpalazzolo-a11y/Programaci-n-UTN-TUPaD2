"""Excepciones propias de Food Store. Todas heredan de FoodStoreError."""


class FoodStoreError(Exception):
    """Error base del sistema: la consola lo captura para mostrar mensajes de negocio."""


class EntidadNoEncontradaError(FoodStoreError):
    """El id solicitado no existe, está eliminado o no pertenece a quien lo pide."""


class DatoInvalidoError(FoodStoreError):
    """Dato con formato incorrecto: texto vacío, tipo equivocado, mail sin '@', etc."""


class PrecioInvalidoError(DatoInvalidoError):
    """El precio es negativo o no es un número válido."""


class StockInvalidoError(DatoInvalidoError):
    """El stock es negativo o no es un entero."""


class CantidadInvalidaError(DatoInvalidoError):
    """La cantidad de un detalle de pedido no es un entero mayor que cero."""


class StockInsuficienteError(FoodStoreError):
    """La cantidad pedida supera el stock disponible del producto."""


class DuplicadoError(FoodStoreError):
    """Mail de usuario o nombre de categoría repetido."""


class OperacionNoPermitidaError(FoodStoreError):
    """Operación que viola una regla de negocio (transición de estado inválida, etc.)."""


class CredencialesInvalidasError(FoodStoreError):
    """Mail o contraseña incorrectos, o usuario eliminado."""
