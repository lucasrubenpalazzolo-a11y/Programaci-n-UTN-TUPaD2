"""Servicio de productos."""

from entidades import Producto
from excepciones import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio
from servicios.utiles import aplicar_cambios


class ProductoServicio:
    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__productos: list[Producto] = []
        self.__categoria_servicio = categoria_servicio

    def listar(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        """Lo que ve el cliente: no eliminados, disponibles y con stock > 0."""
        return [p for p in self.listar() if p.disponible and p.stock > 0]

    def listar_por_categoria(self, categoria_id: int) -> list[Producto]:
        categoria = self.__categoria_servicio.buscar_por_id(categoria_id)
        return [p for p in self.listar() if p.categoria == categoria]

    def buscar_por_id(self, producto_id: int) -> Producto:
        for producto in self.__productos:
            if producto.id == producto_id and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError(f"No existe el producto con id {producto_id}")

    def crear(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria_id: int,
    ) -> Producto:
        categoria = self.__categoria_servicio.buscar_por_id(categoria_id)  # existe y no eliminada
        producto = Producto(nombre, precio, stock, categoria, descripcion, imagen, disponible)
        self.__productos.append(producto)
        return producto

    def editar(
        self,
        producto_id: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        categoria_id: int | None = None,
    ) -> Producto:
        """Modifica solo los campos recibidos (None conserva el valor); todo o nada."""
        producto = self.buscar_por_id(producto_id)
        candidatos: dict[str, object | None] = {
            "nombre": nombre, "descripcion": descripcion, "precio": precio,
            "stock": stock, "imagen": imagen, "disponible": disponible,
        }
        cambios = {k: v for k, v in candidatos.items() if v is not None}
        if categoria_id is not None:
            cambios["categoria"] = self.__categoria_servicio.buscar_por_id(categoria_id)
        aplicar_cambios(producto, cambios)
        return producto

    def eliminar(self, producto_id: int) -> None:
        self.buscar_por_id(producto_id).eliminar()
