"""Lectura validada por teclado. Valida el formato de lo escrito, no reglas de negocio."""

import getpass
import warnings
from enum import Enum
from typing import TypeVar

E = TypeVar("E", bound=Enum)

warnings.simplefilter("ignore", getpass.GetPassWarning)


def leer_texto(mensaje: str) -> str:
    """Texto obligatorio: repite hasta que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede estar vacío.")


def leer_texto_opcional(mensaje: str) -> str | None:
    """Enter devuelve None (conservar el valor anterior)."""
    texto = input(mensaje).strip()
    return texto or None


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_entero_opcional(mensaje: str) -> int | None:
    while True:
        texto = input(mensaje).strip()
        if not texto:
            return None
        try:
            return int(texto)
        except ValueError:
            print("Debe ingresar un número entero.")


def _a_decimal(texto: str) -> float:
    return float(texto.replace(",", "."))


def leer_decimal(mensaje: str) -> float:
    while True:
        try:
            return _a_decimal(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número (por ejemplo 1500 o 1500.50).")


def leer_decimal_opcional(mensaje: str) -> float | None:
    while True:
        texto = input(mensaje).strip()
        if not texto:
            return None
        try:
            return _a_decimal(texto)
        except ValueError:
            print("Debe ingresar un número (por ejemplo 1500 o 1500.50).")


def leer_si_no(mensaje: str) -> bool:
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Responda S o N.")


def leer_si_no_opcional(mensaje: str) -> bool | None:
    while True:
        respuesta = input(mensaje).strip().lower()
        if not respuesta:
            return None
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Responda S o N (o Enter para conservar).")


def leer_contrasenia(mensaje: str) -> str:
    """Oculta lo escrito (getpass); no valida nada."""
    return getpass.getpass(mensaje)


def elegir_enum(tipo: type[E], titulo: str, opcional: bool = False) -> E | None:
    """Muestra los miembros numerados y se elige por número, nunca escribiendo el texto."""
    miembros = list(tipo)
    print(titulo)
    for numero, miembro in enumerate(miembros, start=1):
        print(f"  {numero}. {miembro.name}")
    while True:
        texto = input("Seleccione número" + (" (Enter conserva): " if opcional else ": ")).strip()
        if opcional and not texto:
            return None
        try:
            numero = int(texto)
        except ValueError:
            print("Debe ingresar un número de la lista.")
            continue
        if 1 <= numero <= len(miembros):
            return miembros[numero - 1]
        print("Opción fuera de rango.")


def elegir_enum_obligatorio(tipo: type[E], titulo: str) -> E:
    """Igual que elegir_enum pero nunca devuelve None."""
    elegido = elegir_enum(tipo, titulo, opcional=False)
    assert elegido is not None
    return elegido
