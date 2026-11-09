"""Servicio de categorías: colección en memoria y reglas de negocio."""

from entidades import Categoria
from excepciones import DuplicadoError, EntidadNoEncontradaError, OperacionNoPermitidaError
from servicios.utiles import aplicar_cambios


class CategoriaServicio:
    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        """Categorías no eliminadas."""
        return [c for c in self.__categorias if not c.eliminado]

    def buscar_por_id(self, categoria_id: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == categoria_id and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(f"No existe la categoría con id {categoria_id}")

    def __validar_nombre_unico(self, nombre: str, excepto: Categoria | None = None) -> None:
        for categoria in self.listar():
            if categoria != excepto and categoria.nombre.lower() == nombre.strip().lower():
                raise DuplicadoError(f"Ya existe una categoría llamada '{categoria.nombre}'")

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        categoria = Categoria(nombre, descripcion)  # valida formato
        self.__validar_nombre_unico(categoria.nombre)
        self.__categorias.append(categoria)
        return categoria

    def editar(
        self, categoria_id: int, nombre: str | None = None, descripcion: str | None = None
    ) -> Categoria:
        categoria = self.buscar_por_id(categoria_id)
        cambios: dict[str, object] = {}
        if nombre is not None:
            self.__validar_nombre_unico(nombre, excepto=categoria)
            cambios["nombre"] = nombre
        if descripcion is not None:
            cambios["descripcion"] = descripcion
        aplicar_cambios(categoria, cambios)
        return categoria

    def eliminar(self, categoria_id: int) -> None:
        """Baja lógica; no se permite si tiene productos activos."""
        categoria = self.buscar_por_id(categoria_id)
        activos = categoria.contar_productos_activos()
        if activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría: tiene {activos} producto(s) activo(s)"
            )
        categoria.eliminar()
