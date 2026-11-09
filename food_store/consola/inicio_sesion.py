"""Pantalla de inicio de sesión (hasta 3 intentos)."""

from consola.entrada import leer_contrasenia
from entidades import Usuario
from excepciones import CredencialesInvalidasError
from servicios import UsuarioServicio

MAX_INTENTOS = 3


def iniciar_sesion(usuarios: UsuarioServicio) -> Usuario | None:
    """Devuelve el usuario autenticado, o None si se agotan los intentos."""
    print("\n=== FOOD STORE – INICIO DE SESIÓN ===")
    for intento in range(1, MAX_INTENTOS + 1):
        mail = input("Mail: ").strip()
        contrasenia = leer_contrasenia("Contraseña: ")
        try:
            usuario = usuarios.autenticar(mail, contrasenia)
        except CredencialesInvalidasError as error:
            print(f"✗ {error} (intento {intento} de {MAX_INTENTOS})")
            continue
        print(f"\nBienvenido/a, {usuario.nombre_completo} [{usuario.rol.name}]")
        return usuario
    print("Se agotaron los 3 intentos. El programa finaliza.")
    return None
