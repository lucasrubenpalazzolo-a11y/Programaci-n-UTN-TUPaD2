"""Clase abstracta Menu y utilidades comunes de menús (sin lógica de negocio)."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from consola.entrada import leer_entero
from entidades import Usuario
from excepciones import FoodStoreError

Accion = Callable[[], None]


class Menu(ABC):
    """Menú de un rol. El programa solo llama a mostrar() sin saber qué menú es."""

    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú. True = cerrar sesión, False = salir del programa."""
        ...


def ejecutar(accion: Accion) -> None:
    """Corre una acción capturando errores: un error se informa y se vuelve al menú."""
    try:
        accion()
    except FoodStoreError as error:
        print(f"✗ Error: {error}")
    except ValueError as error:
        print(f"✗ Dato inválido: {error}")


def mostrar_submenu(titulo: str, opciones: dict[int, tuple[str, Accion]]) -> None:
    """Submenú genérico con 0 = Volver. Cada opción es (texto, acción)."""
    while True:
        print(f"\n--- {titulo} ---")
        for numero, (texto, _) in opciones.items():
            print(f"{numero}. {texto}")
        print("0. Volver")
        opcion = leer_entero("Seleccione: ")
        if opcion == 0:
            return
        if opcion in opciones:
            ejecutar(opciones[opcion][1])
        else:
            print("Opción inválida.")


def listar(elementos: list[object], vacio: str) -> None:
    """Imprime un elemento por línea usando su __str__, o el mensaje de lista vacía."""
    if not elementos:
        print(vacio)
    for elemento in elementos:
        print(f"  {elemento}")
