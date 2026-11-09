"""Secciones del menú de administrador: un submenú de alta, baja, modificación y consulta por entidad."""

from consola.entrada import (
    elegir_enum,
    elegir_enum_obligatorio,
    leer_contrasenia,
    leer_decimal,
    leer_decimal_opcional,
    leer_entero,
    leer_entero_opcional,
    leer_si_no,
    leer_si_no_opcional,
    leer_texto,
    leer_texto_opcional,
)
from consola.menu import listar, mostrar_submenu
from consola.menu_cliente import mostrar_detalle_pedido
from entidades import Usuario
from enums import Estado, FormaPago, Rol
from excepciones import DuplicadoError, FoodStoreError
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio


class SeccionCategorias:
    def __init__(self, categorias: CategoriaServicio) -> None:
        self.__s = categorias

    def mostrar(self) -> None:
        mostrar_submenu("CATEGORÍAS", {
            1: ("Listar", self.__listar), 2: ("Crear", self.__crear),
            3: ("Editar", self.__editar), 4: ("Eliminar", self.__eliminar)})

    def __listar(self) -> None:
        listar(list(self.__s.listar()), "No hay categorías cargadas")

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        descripcion = leer_texto("Descripción: ")
        categoria = self.__s.crear(nombre, descripcion)
        print(f"✓ Categoría creada con id {categoria.id}")

    def __editar(self) -> None:
        self.__listar()
        categoria_id = leer_entero("Id de la categoría a editar: ")
        categoria = self.__s.buscar_por_id(categoria_id)
        print(f"Editando: {categoria}  (Enter conserva el valor)")
        nombre = leer_texto_opcional("Nuevo nombre: ")
        descripcion = leer_texto_opcional("Nueva descripción: ")
        self.__s.editar(categoria_id, nombre, descripcion)
        print("✓ Categoría actualizada")

    def __eliminar(self) -> None:
        self.__listar()
        categoria_id = leer_entero("Id de la categoría a eliminar: ")
        if leer_si_no("¿Confirma la eliminación? (S/N): "):
            self.__s.eliminar(categoria_id)
            print("✓ Categoría eliminada")
        else:
            print("Operación cancelada")


class SeccionProductos:
    def __init__(self, productos: ProductoServicio, categorias: CategoriaServicio) -> None:
        self.__s = productos
        self.__categorias = categorias

    def mostrar(self) -> None:
        mostrar_submenu("PRODUCTOS", {
            1: ("Listar", self.__listar), 2: ("Crear", self.__crear),
            3: ("Editar", self.__editar), 4: ("Eliminar", self.__eliminar),
            5: ("Listar por categoría", self.__listar_por_categoria)})

    def __listar(self) -> None:
        listar(list(self.__s.listar()), "No hay productos cargados")

    def __listar_por_categoria(self) -> None:
        listar(list(self.__categorias.listar()), "No hay categorías cargadas")
        categoria_id = leer_entero("Id de la categoría: ")
        listar(list(self.__s.listar_por_categoria(categoria_id)), "No hay productos en esa categoría")

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        descripcion = leer_texto_opcional("Descripción (Enter para dejar vacía): ") or ""
        precio = leer_decimal("Precio: ")
        stock = leer_entero("Stock: ")
        imagen = leer_texto_opcional("Imagen (Enter para dejar vacía): ") or ""
        disponible = leer_si_no("¿Disponible? (S/N): ")
        listar(list(self.__categorias.listar()), "No hay categorías cargadas")
        categoria_id = leer_entero("Id de la categoría: ")
        producto = self.__s.crear(nombre, descripcion, precio, stock, imagen, disponible, categoria_id)
        print(f"✓ Producto creado con id {producto.id}")

    def __editar(self) -> None:
        self.__listar()
        producto_id = leer_entero("Id del producto a editar: ")
        print(f"Editando: {self.__s.buscar_por_id(producto_id)}  (Enter conserva el valor)")
        nombre = leer_texto_opcional("Nuevo nombre: ")
        descripcion = leer_texto_opcional("Nueva descripción: ")
        precio = leer_decimal_opcional("Nuevo precio: ")
        stock = leer_entero_opcional("Nuevo stock: ")
        imagen = leer_texto_opcional("Nueva imagen: ")
        disponible = leer_si_no_opcional("¿Disponible? (S/N): ")
        categoria_id = leer_entero_opcional("Nuevo id de categoría: ")
        self.__s.editar(producto_id, nombre, descripcion, precio, stock, imagen, disponible, categoria_id)
        print("✓ Producto actualizado")

    def __eliminar(self) -> None:
        self.__listar()
        producto_id = leer_entero("Id del producto a eliminar: ")
        if leer_si_no("¿Confirma la eliminación? (S/N): "):
            self.__s.eliminar(producto_id)
            print("✓ Producto eliminado")
        else:
            print("Operación cancelada")


class SeccionUsuarios:
    def __init__(self, usuarios: UsuarioServicio, usuario_en_sesion: Usuario) -> None:
        self.__s = usuarios
        self.__sesion = usuario_en_sesion

    def mostrar(self) -> None:
        mostrar_submenu("USUARIOS", {
            1: ("Listar", self.__listar), 2: ("Crear", self.__crear),
            3: ("Editar", self.__editar), 4: ("Eliminar", self.__eliminar)})

    def __listar(self) -> None:
        listar(list(self.__s.listar()), "No hay usuarios cargados")

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        apellido = leer_texto("Apellido: ")
        celular = leer_texto("Celular: ")
        contrasenia = leer_contrasenia("Contraseña: ")
        rol = elegir_enum_obligatorio(Rol, "Rol:")
        while True:  # si el mail ya existe (o es inválido) se pide otro
            mail = leer_texto("Mail: ")
            try:
                usuario = self.__s.crear(nombre, apellido, mail, celular, contrasenia, rol)
                break
            except DuplicadoError as error:
                print(f"✗ {error}. Ingrese otro.")
            except FoodStoreError as error:
                print(f"✗ {error}. Ingrese otro.")
        print(f"✓ Usuario creado con id {usuario.id}")

    def __editar(self) -> None:
        self.__listar()
        usuario_id = leer_entero("Id del usuario a editar: ")
        print(f"Editando: {self.__s.buscar_por_id(usuario_id)}  (Enter conserva el valor)")
        nombre = leer_texto_opcional("Nuevo nombre: ")
        apellido = leer_texto_opcional("Nuevo apellido: ")
        mail = leer_texto_opcional("Nuevo mail: ")
        celular = leer_texto_opcional("Nuevo celular: ")
        contrasenia = leer_contrasenia("Nueva contraseña (Enter conserva): ") or None
        rol = elegir_enum(Rol, "Nuevo rol:", opcional=True)
        self.__s.editar(usuario_id, self.__sesion, nombre, apellido, mail, celular, contrasenia, rol)
        print("✓ Usuario actualizado")

    def __eliminar(self) -> None:
        self.__listar()
        usuario_id = leer_entero("Id del usuario a eliminar: ")
        if leer_si_no("¿Confirma la eliminación? (S/N): "):
            self.__s.eliminar(usuario_id, self.__sesion)
            print("✓ Usuario eliminado")
        else:
            print("Operación cancelada")


class SeccionPedidos:
    def __init__(self, pedidos: PedidoServicio, usuarios: UsuarioServicio, productos: ProductoServicio) -> None:
        self.__s = pedidos
        self.__usuarios = usuarios
        self.__productos = productos

    def mostrar(self) -> None:
        mostrar_submenu("PEDIDOS", {
            1: ("Listar todos", self.__listar), 2: ("Crear", self.__crear),
            3: ("Cambiar estado y/o forma de pago", self.__actualizar), 4: ("Eliminar", self.__eliminar),
            5: ("Listar por usuario", self.__listar_por_usuario),
            6: ("Ver detalles de un pedido", self.__ver_detalle)})

    def __listar(self) -> None:
        listar(list(self.__s.listar()), "No hay pedidos cargados")

    def __listar_por_usuario(self) -> None:
        listar(list(self.__usuarios.listar()), "No hay usuarios cargados")
        usuario_id = leer_entero("Id del usuario: ")
        listar(list(self.__s.listar_por_usuario(usuario_id)), "Ese usuario no tiene pedidos")

    def __ver_detalle(self) -> None:
        self.__listar()
        mostrar_detalle_pedido(self.__s.buscar_por_id(leer_entero("Id del pedido: ")))

    def __crear(self) -> None:
        listar(list(self.__usuarios.listar()), "No hay usuarios cargados")
        usuario_id = leer_entero("Id del usuario: ")
        forma_pago = elegir_enum_obligatorio(FormaPago, "Forma de pago:")
        try:
            pedido = self.__s.iniciar_pedido(usuario_id, forma_pago)
            listar(list(self.__productos.listar_disponibles()), "No hay productos disponibles")
            while True:
                producto_id = leer_entero("Id del producto: ")
                cantidad = leer_entero("Cantidad: ")
                self.__s.agregar_item(pedido, producto_id, cantidad)
                print("✓ Detalle agregado")
                if not leer_si_no("¿Agregar otro producto? (S/N): "):
                    break
            self.__s.confirmar_creacion(pedido)
        except FoodStoreError as error:
            print(f"✗ {error}")
            print("Creación del pedido cancelada: no se guardó el pedido ni se modificó el stock.")
            return
        print(f"✓ Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")

    def __actualizar(self) -> None:
        self.__listar()
        pedido_id = leer_entero("Id del pedido: ")
        pedido = self.__s.buscar_por_id(pedido_id)
        print(f"Editando: {pedido}  (Enter conserva el valor)")
        estado = elegir_enum(Estado, "Nuevo estado:", opcional=True)
        forma_pago = elegir_enum(FormaPago, "Nueva forma de pago:", opcional=True)
        self.__s.actualizar(pedido_id, estado, forma_pago)
        print("✓ Pedido actualizado")

    def __eliminar(self) -> None:
        self.__listar()
        pedido_id = leer_entero("Id del pedido a eliminar: ")
        if leer_si_no("¿Confirma la eliminación? (S/N): "):
            self.__s.eliminar(pedido_id)
            print("✓ Pedido eliminado")
        else:
            print("Operación cancelada")
