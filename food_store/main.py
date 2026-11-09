"""Food Store - punto de entrada. Solo arma los servicios y arranca el menú principal."""

from consola.fabrica_menu import crear_menu
from consola.inicio_sesion import iniciar_sesion
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio
from servicios.datos_iniciales import cargar_datos_iniciales


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio(usuarios, productos)
    cargar_datos_iniciales(categorias, productos, usuarios, pedidos)

    try:
        while True:
            usuario = iniciar_sesion(usuarios)  # la sesión es una variable local
            if usuario is None:
                break
            menu = crear_menu(usuario, categorias, productos, usuarios, pedidos)
            if not menu.mostrar():  # False = salir del programa
                break
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido.")
    print("¡Hasta luego!")


if __name__ == "__main__":
    main()
