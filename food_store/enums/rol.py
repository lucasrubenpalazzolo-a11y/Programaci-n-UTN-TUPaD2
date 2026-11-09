"""Enumerado Rol: define los dos tipos de usuario del sistema."""

from enum import Enum


class Rol(Enum):
    """Rol de un usuario: ADMIN gestiona todo, USUARIO (cliente) solo consulta."""

    ADMIN = "Administrador"
    USUARIO = "Cliente"
