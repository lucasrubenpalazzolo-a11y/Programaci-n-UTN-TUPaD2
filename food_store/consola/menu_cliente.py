"""Menú del rol USUARIO (cliente): solo consulta."""

from consola.entrada import leer_entero, leer_entero_opcional
from consola.menu import Menu, ejecutar, listar
from entidades import Pedido, Usuario
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio


def mostrar_detalle_pedido(pedido: Pedido) -> None:
    print(f"Pedido {pedido}")
    for detalle in pedido.detalles:
        print(f"    - {detalle}")
    print(f"    TOTAL: ${pedido.total:.2f}")


class MenuCliente(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        pedidos: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categorias = categorias
        self.__productos = productos
        self.__pedidos = pedidos

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – CLIENTE ({self._usuario.nombre_completo}) ===")
            print("1. Ver categorías\n2. Ver productos disponibles\n3. Mis pedidos\n4. Mis datos")
            print("9. Cerrar sesión\n0. Salir")
            opcion = leer_entero("Seleccione: ")
            if opcion == 9:
                return True
            if opcion == 0:
                return False
            acciones = {1: self.__ver_categorias, 2: self.__ver_productos,
                        3: self.__mis_pedidos, 4: self.__mis_datos}
            if opcion in acciones:
                ejecutar(acciones[opcion])
            else:
                print("Opción inválida.")

    def __ver_categorias(self) -> None:
        listar(list(self.__categorias.listar()), "No hay categorías cargadas")

    def __ver_productos(self) -> None:
        listar(list(self.__productos.listar_disponibles()), "No hay productos disponibles")

    def __mis_pedidos(self) -> None:
        listar(list(self.__pedidos.listar_por_usuario(self._usuario.id)), "No tiene pedidos")
        pedido_id = leer_entero_opcional("Id del pedido para ver detalles (Enter para volver): ")
        if pedido_id is not None:
            mostrar_detalle_pedido(self.__pedidos.buscar_de_usuario(pedido_id, self._usuario))

    def __mis_datos(self) -> None:
        u = self._usuario
        print(f"Nombre: {u.nombre}\nApellido: {u.apellido}\nMail: {u.mail}\n"
              f"Celular: {u.celular}\nRol: {u.rol.name}")
