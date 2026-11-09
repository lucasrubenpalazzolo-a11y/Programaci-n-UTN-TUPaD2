"""Servicio de usuarios y autenticación."""

from entidades import Usuario
from enums import Rol
from excepciones import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)
from servicios.utiles import aplicar_cambios


class UsuarioServicio:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == usuario_id and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(f"No existe el usuario con id {usuario_id}")

    def __validar_mail_unico(self, mail: str, excepto: Usuario | None = None) -> None:
        for usuario in self.listar():
            if usuario != excepto and usuario.mail == mail.strip().lower():
                raise DuplicadoError(f"El mail '{usuario.mail}' ya está registrado")

    def crear(
        self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol
    ) -> Usuario:
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__validar_mail_unico(usuario.mail)
        self.__usuarios.append(usuario)
        return usuario

    def editar(
        self,
        usuario_id: int,
        usuario_en_sesion: Usuario,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        """Modifica solo los campos recibidos; un admin no puede quitarse su propio rol."""
        usuario = self.buscar_por_id(usuario_id)
        if mail is not None:
            self.__validar_mail_unico(mail, excepto=usuario)
        if rol is not None and usuario == usuario_en_sesion and rol != usuario.rol:
            raise OperacionNoPermitidaError("No puede cambiar su propio rol mientras tiene la sesión iniciada")
        candidatos: dict[str, object | None] = {
            "nombre": nombre, "apellido": apellido, "mail": mail, "celular": celular, "rol": rol,
        }
        aplicar_cambios(usuario, {k: v for k, v in candidatos.items() if v is not None})
        if contrasenia is not None:  # sin getter: se aplica al final, cuando lo demás ya salió bien
            usuario.contrasenia = contrasenia
        return usuario

    def eliminar(self, usuario_id: int, usuario_en_sesion: Usuario) -> None:
        usuario = self.buscar_por_id(usuario_id)
        if usuario == usuario_en_sesion:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a sí mismo")
        usuario.eliminar()

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Mismo mensaje para mail inexistente, usuario eliminado o contraseña incorrecta."""
        for usuario in self.listar():
            if usuario.mail == mail.strip().lower() and usuario.verificar_contrasenia(contrasenia):
                return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")
