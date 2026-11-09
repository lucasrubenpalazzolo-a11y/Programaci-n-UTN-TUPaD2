"""Datos que carga main(): administrador inicial y datos de ejemplo."""

from enums import FormaPago, Rol
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

ADMIN_MAIL = "admin@foodstore.com"
ADMIN_CONTRASENIA = "admin123"
CLIENTE_MAIL = "juan@mail.com"
CLIENTE_CONTRASENIA = "juan123"


def cargar_datos_iniciales(
    categorias: CategoriaServicio,
    productos: ProductoServicio,
    usuarios: UsuarioServicio,
    pedidos: PedidoServicio,
) -> None:
    """Crea el administrador (sin él nadie podría ingresar) y datos de ejemplo."""
    usuarios.crear("Ana", "Pérez", ADMIN_MAIL, "3815550001", ADMIN_CONTRASENIA, Rol.ADMIN)
    juan = usuarios.crear("Juan", "Gómez", CLIENTE_MAIL, "3815550002", CLIENTE_CONTRASENIA, Rol.USUARIO)
    pizzas = categorias.crear("Pizzas", "Pizzas al horno de piedra")
    burgers = categorias.crear("Hamburguesas", "Hamburguesas de carne y vegetarianas")
    bebidas = categorias.crear("Bebidas", "Gaseosas, aguas y cervezas")
    postres = categorias.crear("Postres", "Dulces caseros")
    muzza = productos.crear("Pizza Muzzarella", "Muzzarella y orégano", 9500.0, 20, "muzza.jpg", True, pizzas.id)
    productos.crear("Pizza Napolitana", "Tomate, ajo y albahaca", 11000.0, 15, "napo.jpg", True, pizzas.id)
    productos.crear("Hamburguesa Clásica", "Carne, queso y lechuga", 8000.0, 25, "clasica.jpg", True, burgers.id)
    productos.crear("Hamburguesa Veggie", "Medallón de lentejas", 8500.0, 10, "veggie.jpg", True, burgers.id)
    cola = productos.crear("Gaseosa 500ml", "Línea cola", 2500.0, 50, "cola.jpg", True, bebidas.id)
    productos.crear("Cerveza Artesanal", "IPA 473ml", 4000.0, 30, "ipa.jpg", True, bebidas.id)
    productos.crear("Tiramisú", "Porción individual", 5000.0, 2, "tira.jpg", True, postres.id)
    productos.crear("Flan Casero", "Con dulce de leche", 4500.0, 8, "flan.jpg", False, postres.id)
    pedidos.crear(juan.id, FormaPago.EFECTIVO, [(muzza.id, 1), (cola.id, 2)])
