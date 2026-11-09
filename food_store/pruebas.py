"""Pruebas del modelo y de los servicios (sin menú). Ejecutar: python pruebas.py

Muestra en pantalla los casos válidos (OK) y los errores esperados (ERROR ESPERADO).
"""

import ast
import sys
from collections.abc import Callable
from pathlib import Path

from entidades import Base, Calculable, Categoria, Pedido, Producto, Usuario
from enums import Estado, FormaPago, Rol
from excepciones import (
    CantidadInvalidaError,
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    FoodStoreError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
    StockInvalidoError,
)
from consola.fabrica_menu import crear_menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio

fallos: list[str] = []
total_pruebas = 0


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def ok(descripcion: str, condicion: bool) -> None:
    """Caso válido: la condición debe cumplirse."""
    global total_pruebas
    total_pruebas += 1
    if condicion:
        print(f"  [OK]              {descripcion}")
    else:
        print(f"  [FALLO]           {descripcion}")
        fallos.append(descripcion)


def error(descripcion: str, tipo: type[Exception], accion: Callable[[], object]) -> None:
    """Caso inválido: la acción debe lanzar la excepción indicada."""
    global total_pruebas
    total_pruebas += 1
    try:
        accion()
    except tipo as e:
        print(f"  [ERROR ESPERADO]  {descripcion} -> {tipo.__name__}: {e}")
    except Exception as e:  # excepción de otro tipo
        print(f"  [FALLO]           {descripcion} -> lanzó {type(e).__name__} en vez de {tipo.__name__}")
        fallos.append(descripcion)
    else:
        print(f"  [FALLO]           {descripcion} -> no lanzó {tipo.__name__}")
        fallos.append(descripcion)


def armar() -> tuple[CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio]:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    return categorias, productos, usuarios, PedidoServicio(usuarios, productos)


def probar_modelo() -> None:
    titulo("MODELO: Base, Calculable y enumerados")
    error("Base es abstracta y no se instancia", TypeError, lambda: Base())  # type: ignore[abstract]
    error("Calculable es una interfaz y no se instancia", TypeError, lambda: Calculable())  # type: ignore[abstract]
    c1, c2 = Categoria("A", "desc"), Categoria("B", "desc")
    ok("ids autoincrementales por clase", c2.id == c1.id + 1)
    ok("creado_en se asigna solo", c1.creado_en is not None and not c1.eliminado)
    ok("__eq__ compara por id (misma instancia y distinto id)", c1 == c1 and c1 != c2)
    ok("__hash__ coherente con __eq__", len({c1, c2, c1}) == 2)
    ok("Estado: PENDIENTE -> CONFIRMADO es válida", Estado.PENDIENTE.puede_pasar_a(Estado.CONFIRMADO))
    ok("Estado: PENDIENTE -> TERMINADO no es válida", not Estado.PENDIENTE.puede_pasar_a(Estado.TERMINADO))
    ok("Estado: TERMINADO y CANCELADO son finales", Estado.TERMINADO.es_final and Estado.CANCELADO.es_final)

    titulo("MODELO: Categoria y Producto")
    error("Categoria con nombre vacío", DatoInvalidoError, lambda: Categoria("  ", "x"))
    error("Categoria con descripción vacía", DatoInvalidoError, lambda: Categoria("x", ""))
    cat = Categoria("Pizzas", "Al horno")
    p = Producto("Muzza", 100.0, 5, cat)
    ok("Producto válido y asociado a su categoría (ambos lados)", p.categoria == cat and p in cat.productos)
    error("Producto con precio negativo", PrecioInvalidoError, lambda: Producto("x", -1.0, 1, cat))
    error("Producto con stock negativo", StockInvalidoError, lambda: Producto("x", 1.0, -1, cat))
    error("Producto con nombre vacío", DatoInvalidoError, lambda: Producto("", 1.0, 1, cat))
    error("Producto sin categoría válida", DatoInvalidoError, lambda: Producto("x", 1.0, 1, None))  # type: ignore[arg-type]

    def poner_precio_negativo() -> None:
        p.precio = -5.0

    error("Setter de precio valida (negativo)", PrecioInvalidoError, poner_precio_negativo)
    ok("El precio no cambió tras el error", p.precio == 100.0)
    otra = Categoria("Bebidas", "x")
    p.categoria = otra
    ok("Cambiar categoría actualiza ambos lados", p in otra.productos and p not in cat.productos)
    ok("productos devuelve una tupla (inmutable)", isinstance(otra.productos, tuple))
    ok("__str__ útil de Producto", "Muzza" in str(p) and "$100.00" in str(p))

    titulo("MODELO: Usuario")
    u = Usuario("Ana", "Pérez", "Ana@Mail.com", "123", "secreta", Rol.ADMIN)
    ok("verificar_contrasenia correcta", u.verificar_contrasenia("secreta"))
    ok("verificar_contrasenia incorrecta", not u.verificar_contrasenia("otra"))
    ok("mail se normaliza a minúsculas", u.mail == "ana@mail.com")
    ok("__str__ no muestra la contraseña", "secreta" not in str(u))
    error("La contraseña no tiene getter", AttributeError, lambda: u.contrasenia)
    error("Mail sin '@'", DatoInvalidoError, lambda: Usuario("a", "b", "mail.com", "1", "x", Rol.ADMIN))
    error("Mail vacío", DatoInvalidoError, lambda: Usuario("a", "b", "", "1", "x", Rol.ADMIN))
    error("Contraseña vacía", DatoInvalidoError, lambda: Usuario("a", "b", "a@b.c", "1", "", Rol.ADMIN))

    titulo("MODELO: Pedido y DetallePedido (composición)")
    cliente = Usuario("Juan", "Gómez", "juan@mail.com", "1", "j", Rol.USUARIO)
    a = Producto("A", 100.0, 10, cat)
    b = Producto("B", 50.5, 3, cat)
    ped = Pedido(cliente, FormaPago.EFECTIVO)
    ok("Pedido arranca PENDIENTE, total 0 y es Calculable", ped.estado == Estado.PENDIENTE and ped.total == 0 and isinstance(ped, Calculable))
    ped.agregar_detalle(2, a)
    ped.agregar_detalle(1, b)
    ok("subtotal = cantidad x precio del producto", ped.buscar_detalle_por_producto(a).subtotal == 200.0)  # type: ignore[union-attr]
    ok("total calculado con calcular_total()", ped.total == 250.5)
    ped.agregar_detalle(3, a)
    ok("mismo producto: se suma la cantidad al detalle existente", len(ped.detalles) == 2 and ped.buscar_detalle_por_producto(a).cantidad == 5)  # type: ignore[union-attr]
    error("Cantidad 0", CantidadInvalidaError, lambda: ped.agregar_detalle(0, b))
    error("Cantidad negativa", CantidadInvalidaError, lambda: ped.agregar_detalle(-2, b))
    error("Cantidad mayor al stock", StockInsuficienteError, lambda: ped.agregar_detalle(3, b))
    error("Suma de cantidades mayor al stock", StockInsuficienteError, lambda: ped.agregar_detalle(6, a))
    ok("detalles devuelve una tupla (no se puede modificar desde afuera)", isinstance(ped.detalles, tuple))
    ped.eliminar_detalle_por_producto(b)
    ok("eliminar_detalle_por_producto recalcula el total", len(ped.detalles) == 1 and ped.total == 500.0)
    error("Eliminar detalle de producto inexistente", EntidadNoEncontradaError, lambda: ped.eliminar_detalle_por_producto(b))
    a.precio = 999.0
    ok("Cambiar el precio después no altera el subtotal ya armado", ped.total == 500.0)
    error("Pedido sin usuario", DatoInvalidoError, lambda: Pedido(None, FormaPago.EFECTIVO))  # type: ignore[arg-type]
    eliminado = Usuario("X", "Y", "x@y.com", "1", "x", Rol.USUARIO)
    eliminado.eliminar()
    error("Pedido con usuario eliminado", OperacionNoPermitidaError, lambda: Pedido(eliminado, FormaPago.EFECTIVO))
    error("Producto no disponible no se agrega", OperacionNoPermitidaError, lambda: ped.agregar_detalle(1, Producto("N", 1.0, 5, cat, disponible=False)))

    def a_terminado() -> None:
        ped.estado = Estado.TERMINADO

    error("PENDIENTE -> TERMINADO es inválida", OperacionNoPermitidaError, a_terminado)
    ped.estado = Estado.CONFIRMADO
    ped.estado = Estado.TERMINADO
    ok("PENDIENTE -> CONFIRMADO -> TERMINADO es válida", ped.estado == Estado.TERMINADO)

    def volver() -> None:
        ped.estado = Estado.CANCELADO

    error("TERMINADO no cambia más", OperacionNoPermitidaError, volver)
    error("Un pedido final no admite cambiar la forma de pago", OperacionNoPermitidaError, lambda: setattr(ped, "forma_pago", FormaPago.TARJETA))
    ok("__str__ útil de Pedido", "Juan Gómez" in str(ped) and "TERMINADO" in str(ped))


def probar_categorias() -> None:
    titulo("SERVICIOS: categorías")
    categorias, productos, _, _ = armar()
    c = categorias.crear("Pizzas", "Al horno")
    ok("crear categoría y listarla", c in categorias.listar())
    error("Nombre repetido (sin distinguir mayúsculas)", DuplicadoError, lambda: categorias.crear("PIZZAS", "otra"))
    error("Buscar id inexistente", EntidadNoEncontradaError, lambda: categorias.buscar_por_id(999))
    categorias.editar(c.id, nombre="Pizzas Gourmet")
    ok("editar nombre (descripción se conserva)", c.nombre == "Pizzas Gourmet" and c.descripcion == "Al horno")
    otra = categorias.crear("Bebidas", "x")
    error("Editar con nombre de otra categoría", DuplicadoError, lambda: categorias.editar(otra.id, nombre="pizzas gourmet"))
    prod = productos.crear("Muzza", "x", 10.0, 5, "", True, c.id)
    error("Eliminar categoría con productos activos", OperacionNoPermitidaError, lambda: categorias.eliminar(c.id))
    productos.eliminar(prod.id)
    categorias.eliminar(c.id)
    ok("eliminar sin productos activos: baja lógica y desaparece del listado", c.eliminado and c not in categorias.listar())
    error("Editar categoría eliminada", EntidadNoEncontradaError, lambda: categorias.editar(c.id, nombre="x"))


def probar_productos() -> None:
    titulo("SERVICIOS: productos")
    categorias, productos, _, _ = armar()
    c = categorias.crear("Pizzas", "x")
    p = productos.crear("Muzza", "x", 100.0, 5, "m.jpg", True, c.id)
    ok("crear producto", p in productos.listar())
    error("Crear con categoría inexistente", EntidadNoEncontradaError, lambda: productos.crear("x", "", 1.0, 1, "", True, 999))
    error("Crear con precio negativo", PrecioInvalidoError, lambda: productos.crear("x", "", -1.0, 1, "", True, c.id))
    error("Crear con stock negativo", StockInvalidoError, lambda: productos.crear("x", "", 1.0, -1, "", True, c.id))
    error("Editar con precio inválido (todo o nada)", PrecioInvalidoError, lambda: productos.editar(p.id, nombre="Nuevo", precio=-5.0))
    ok("tras el error no cambió ningún campo", p.nombre == "Muzza" and p.precio == 100.0)
    productos.editar(p.id, precio=120.0, stock=7)
    ok("editar varios campos", p.precio == 120.0 and p.stock == 7)
    productos.crear("Sin stock", "", 10.0, 0, "", True, c.id)
    productos.crear("No disp", "", 10.0, 5, "", False, c.id)
    ok("el cliente ve solo disponibles con stock > 0", [x.nombre for x in productos.listar_disponibles()] == ["Muzza"])
    productos.eliminar(p.id)
    ok("eliminar producto: baja lógica", p.eliminado and p not in productos.listar())
    error("Editar producto eliminado", EntidadNoEncontradaError, lambda: productos.editar(p.id, nombre="x"))


def probar_usuarios() -> None:
    titulo("SERVICIOS: usuarios y autenticación")
    _, _, usuarios, _ = armar()
    admin = usuarios.crear("Ana", "Pérez", "admin@foodstore.com", "1", "admin123", Rol.ADMIN)
    cli = usuarios.crear("Juan", "Gómez", "juan@mail.com", "2", "juan123", Rol.USUARIO)
    error("Mail repetido", DuplicadoError, lambda: usuarios.crear("x", "y", "JUAN@mail.com", "1", "z", Rol.USUARIO))
    ok("autenticar correcto", usuarios.autenticar("admin@foodstore.com", "admin123") == admin)
    for desc, mail, clave in [("mail inexistente", "no@existe.com", "x"), ("contraseña incorrecta", "juan@mail.com", "mal")]:
        error(f"Login con {desc}", CredencialesInvalidasError, lambda m=mail, c=clave: usuarios.autenticar(m, c))  # type: ignore[misc]
    error("Admin no puede eliminarse a sí mismo", OperacionNoPermitidaError, lambda: usuarios.eliminar(admin.id, admin))
    ok("el admin sigue activo", not admin.eliminado)
    error("Admin no puede quitarse su rol", OperacionNoPermitidaError, lambda: usuarios.editar(admin.id, admin, rol=Rol.USUARIO))
    error("Editar mail a uno existente", DuplicadoError, lambda: usuarios.editar(cli.id, admin, mail="admin@foodstore.com"))
    usuarios.editar(cli.id, admin, nombre="Juan Carlos", contrasenia="nueva")
    ok("editar nombre y contraseña", cli.nombre == "Juan Carlos" and usuarios.autenticar("juan@mail.com", "nueva") == cli)
    usuarios.eliminar(cli.id, admin)
    ok("eliminar usuario: baja lógica y sale del listado", cli.eliminado and cli not in usuarios.listar())
    msgs = set()
    for mail, clave in [("juan@mail.com", "nueva"), ("no@existe.com", "x"), ("admin@foodstore.com", "mal")]:
        try:
            usuarios.autenticar(mail, clave)
        except CredencialesInvalidasError as e:
            msgs.add(str(e))
    ok("usuario eliminado no inicia sesión y el mensaje es el mismo en los 3 casos", len(msgs) == 1)


def probar_pedidos() -> None:
    titulo("SERVICIOS: pedidos")
    categorias, productos, usuarios, pedidos = armar()
    c = categorias.crear("Comida", "x")
    p1 = productos.crear("Pizza", "", 100.0, 10, "", True, c.id)
    p2 = productos.crear("Tiramisú", "", 50.0, 2, "", True, c.id)
    ana = usuarios.crear("Ana", "P", "ana@m.com", "1", "a", Rol.ADMIN)
    juan = usuarios.crear("Juan", "G", "juan@m.com", "1", "j", Rol.USUARIO)

    ped = pedidos.crear(juan.id, FormaPago.TARJETA, [(p1.id, 3), (p2.id, 1)])
    ok("pedido creado: total correcto y stock descontado", ped.total == 350.0 and p1.stock == 7 and p2.stock == 1)
    ok("el pedido está en la colección", ped in pedidos.listar())

    error("Falta de stock cancela la creación", StockInsuficienteError, lambda: pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 2), (p2.id, 5)]))
    ok("no se agregó el pedido ni se tocó el stock", len(pedidos.listar()) == 1 and p1.stock == 7 and p2.stock == 1)
    error("Pedido con usuario inexistente", EntidadNoEncontradaError, lambda: pedidos.crear(999, FormaPago.EFECTIVO, [(p1.id, 1)]))
    error("Pedido sin detalles", DatoInvalidoError, lambda: pedidos.crear(juan.id, FormaPago.EFECTIVO, []))
    error("Cantidad 0 en un detalle", CantidadInvalidaError, lambda: pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 0)]))
    anulado = usuarios.crear("Baja", "X", "baja@m.com", "1", "b", Rol.USUARIO)
    usuarios.eliminar(anulado.id, ana)
    error("Pedido con usuario eliminado", EntidadNoEncontradaError, lambda: pedidos.crear(anulado.id, FormaPago.EFECTIVO, [(p1.id, 1)]))

    error("Transición inválida PENDIENTE -> TERMINADO", OperacionNoPermitidaError, lambda: pedidos.actualizar(ped.id, estado=Estado.TERMINADO))
    ok("no cambió nada tras la transición inválida", ped.estado == Estado.PENDIENTE)
    pedidos.actualizar(ped.id, estado=Estado.CONFIRMADO, forma_pago=FormaPago.TRANSFERENCIA)
    ok("estado y forma de pago actualizados", ped.estado == Estado.CONFIRMADO and ped.forma_pago == FormaPago.TRANSFERENCIA)
    pedidos.actualizar(ped.id, estado=Estado.CANCELADO)
    ok("cancelar devuelve el stock", ped.estado == Estado.CANCELADO and p1.stock == 10 and p2.stock == 2)
    error("CANCELADO no cambia más", OperacionNoPermitidaError, lambda: pedidos.actualizar(ped.id, estado=Estado.CONFIRMADO))

    ped2 = pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 4)])
    pedidos.eliminar(ped2.id)
    ok("eliminar pedido no terminado devuelve stock, marca pedido y detalles", p1.stock == 10 and ped2.eliminado and all(d.eliminado for d in ped2.detalles))
    ok("el pedido eliminado no aparece en listados", ped2 not in pedidos.listar())
    error("Buscar pedido eliminado", EntidadNoEncontradaError, lambda: pedidos.buscar_por_id(ped2.id))

    ped3 = pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 2)])
    pedidos.actualizar(ped3.id, estado=Estado.CONFIRMADO)
    pedidos.actualizar(ped3.id, estado=Estado.TERMINADO)
    pedidos.eliminar(ped3.id)
    ok("eliminar pedido TERMINADO no devuelve stock", p1.stock == 8)

    ped4 = pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 1)])
    ok("cada usuario ve solo sus pedidos", ped4 in pedidos.listar_por_usuario(juan.id) and not pedidos.listar_por_usuario(ana.id))
    error("Pedido de otro usuario se informa como inexistente", EntidadNoEncontradaError, lambda: pedidos.buscar_de_usuario(ped4.id, ana))
    productos.eliminar(p1.id)
    ok("producto eliminado: el pedido existente se sigue mostrando", "Pizza" in str(ped4.detalles[0]) and ped4 in pedidos.listar())
    error("Producto eliminado no se agrega a pedidos nuevos", EntidadNoEncontradaError, lambda: pedidos.crear(juan.id, FormaPago.EFECTIVO, [(p1.id, 1)]))


def probar_menus() -> None:
    titulo("CONSOLA: polimorfismo de menús (sin interacción)")
    c, p, u, pe = armar()
    admin = u.crear("Ana", "P", "ana@m.com", "1", "a", Rol.ADMIN)
    cli = u.crear("Juan", "G", "juan@m.com", "1", "j", Rol.USUARIO)
    ok("crear_menu(ADMIN) devuelve MenuAdministrador", isinstance(crear_menu(admin, c, p, u, pe), MenuAdministrador))
    ok("crear_menu(USUARIO) devuelve MenuCliente", isinstance(crear_menu(cli, c, p, u, pe), MenuCliente))
    error("Un cliente no puede abrir el menú de administrador", OperacionNoPermitidaError, lambda: MenuAdministrador(cli, c, p, u, pe))


def probar_arquitectura() -> None:
    titulo("ARQUITECTURA: capas (consola -> servicios -> entidades)")
    raiz = Path(__file__).parent

    def llamadas(carpeta: str) -> set[str]:
        usadas: set[str] = set()
        for archivo in (raiz / carpeta).glob("*.py"):
            for nodo in ast.walk(ast.parse(archivo.read_text(encoding="utf-8"))):
                if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
                    usadas.add(nodo.func.id)
        return usadas

    def importa(carpeta: str, prohibidos: tuple[str, ...]) -> bool:
        for archivo in (raiz / carpeta).glob("*.py"):
            for nodo in ast.walk(ast.parse(archivo.read_text(encoding="utf-8"))):
                if isinstance(nodo, ast.ImportFrom) and nodo.module and nodo.module.split(".")[0] in prohibidos:
                    return True
        return False

    ok("entidades no usan input() ni print()", not ({"input", "print"} & llamadas("entidades")))
    ok("servicios no usan input() ni print()", not ({"input", "print"} & llamadas("servicios")))
    ok("entidades no importan servicios ni consola", not importa("entidades", ("servicios", "consola")))
    ok("servicios no importan consola", not importa("servicios", ("consola",)))


def main() -> None:
    probar_modelo()
    probar_categorias()
    probar_productos()
    probar_usuarios()
    probar_pedidos()
    probar_menus()
    probar_arquitectura()
    print(f"\nResumen: {total_pruebas - len(fallos)}/{total_pruebas} pruebas correctas.")
    if fallos:
        print("Fallaron:", *fallos, sep="\n  - ")
        sys.exit(1)
    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    try:
        main()
    except FoodStoreError as e:  # un error no previsto del dominio no debería escapar
        print(f"Error inesperado: {e}")
        sys.exit(1)
