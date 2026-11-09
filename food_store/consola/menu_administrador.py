"""Menú del rol ADMIN: gestión completa."""

from consola.entrada import leer_entero
from consola.menu import Menu, ejecutar
from consola.secciones_admin import (
    SeccionCategorias,
    SeccionPedidos,
    SeccionProductos,
    SeccionUsuarios,
)
from entidades import Usuario
from enums import Rol
from excepciones import OperacionNoPermitidaError
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio


Seccion = SeccionCategorias | SeccionProductos | SeccionUsuarios | SeccionPedidos


class MenuAdministrador(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        usuarios: UsuarioServicio,
        pedidos: PedidoServicio,
    ) -> None:
        if usuario.rol != Rol.ADMIN:  # defensa extra: solo un ADMIN gestiona datos
            raise OperacionNoPermitidaError("Solo un ADMIN puede usar el menú de administrador")
        super().__init__(usuario)
        self.__secciones: dict[int, Seccion] = {
            1: SeccionCategorias(categorias),
            2: SeccionProductos(productos, categorias),
            3: SeccionUsuarios(usuarios, usuario),
            4: SeccionPedidos(pedidos, usuarios, productos),
        }

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre_completo}) ===")
            print("1. Categorías\n2. Productos\n3. Usuarios\n4. Pedidos\n9. Cerrar sesión\n0. Salir")
            opcion = leer_entero("Seleccione: ")
            if opcion == 9:
                return True
            if opcion == 0:
                return False
            if opcion in self.__secciones:
                ejecutar(self.__secciones[opcion].mostrar)
            else:
                print("Opción inválida.")
