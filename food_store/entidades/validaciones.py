"""Validaciones reutilizables por los setters de las entidades."""

import math

from excepciones import (
    CantidadInvalidaError,
    DatoInvalidoError,
    PrecioInvalidoError,
    StockInvalidoError,
)


def validar_texto(valor: object, campo: str) -> str:
    """Devuelve el texto sin espacios en los bordes; falla si no es str o queda vacío."""
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"El campo '{campo}' no puede estar vacío")
    return valor.strip()


def validar_texto_opcional(valor: object, campo: str) -> str:
    """Como validar_texto, pero admite texto vacío (por ejemplo, descripción o imagen)."""
    if not isinstance(valor, str):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser texto")
    return valor.strip()


def validar_booleano(valor: object, campo: str) -> bool:
    """Falla si el valor no es un booleano."""
    if not isinstance(valor, bool):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser verdadero o falso")
    return valor


def validar_precio(valor: object) -> float:
    """El precio debe ser un número finito mayor o igual a cero."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise PrecioInvalidoError("El precio debe ser un número")
    if not math.isfinite(valor):
        raise PrecioInvalidoError("El precio debe ser un número finito")
    if valor < 0:
        raise PrecioInvalidoError("El precio no puede ser negativo")
    return float(valor)


def validar_stock(valor: object) -> int:
    """El stock debe ser un entero mayor o igual a cero."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise StockInvalidoError("El stock debe ser un número entero")
    if valor < 0:
        raise StockInvalidoError("El stock no puede ser negativo")
    return valor


def validar_cantidad(valor: object) -> int:
    """La cantidad de un detalle debe ser un entero mayor que cero."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise CantidadInvalidaError("La cantidad debe ser un número entero")
    if valor <= 0:
        raise CantidadInvalidaError("La cantidad debe ser mayor que cero")
    return valor


def validar_mail(valor: object) -> str:
    """Formato básico de mail: no vacío y con '@' y '.'. Se guarda en minúsculas."""
    texto = validar_texto(valor, "mail").lower()
    if "@" not in texto or "." not in texto or " " in texto:
        raise DatoInvalidoError("El mail no tiene un formato válido (debe contener '@' y '.')")
    return texto
