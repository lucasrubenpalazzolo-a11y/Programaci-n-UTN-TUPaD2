"""Entidad Usuario: persona que inicia sesión (rol ADMIN o USUARIO)."""

from entidades.base import Base
from entidades.validaciones import validar_mail, validar_texto
from enums import Rol
from excepciones import DatoInvalidoError


class Usuario(Base):
    """Usuario del sistema. La contraseña nunca sale del objeto."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.__nombre: str = validar_texto(nombre, "nombre")
        self.__apellido: str = validar_texto(apellido, "apellido")
        self.__mail: str = validar_mail(mail)
        self.__celular: str = validar_texto(celular, "celular")
        self.__contrasenia: str = self.__validar_contrasenia(contrasenia)
        self.__rol: Rol = self.__validar_rol(rol)

    @staticmethod
    def __validar_contrasenia(valor: object) -> str:
        if not isinstance(valor, str) or not valor:
            raise DatoInvalidoError("La contraseña no puede estar vacía")
        return valor

    @staticmethod
    def __validar_rol(valor: object) -> Rol:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser ADMIN o USUARIO")
        return valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = validar_texto(valor, "nombre")

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        self.__apellido = validar_texto(valor, "apellido")

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        """El formato se valida aquí; la unicidad la controla UsuarioServicio."""
        self.__mail = validar_mail(valor)

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = validar_texto(valor, "celular")

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        self.__rol = self.__validar_rol(valor)

    def _cambiar_contrasenia(self, valor: str) -> None:
        self.__contrasenia = self.__validar_contrasenia(valor)

    # Propiedad de solo escritura: no tiene getter, así la contraseña no se puede leer.
    contrasenia = property(fset=_cambiar_contrasenia, doc="Solo escritura; use verificar_contrasenia().")

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Compara la contraseña ingresada con la guardada, sin exponerla."""
        return self.__contrasenia == contrasenia

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre_completo} | {self.mail} | {self.rol.name}"
