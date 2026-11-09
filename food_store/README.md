# Food Store – Sistema de Gestión de Pedidos de Comida (consola)

**Universidad Tecnológica Nacional – Facultad Regional Mendoza · Tecnicatura Universitaria en Programación a Distancia · Programación II · Entrega: 09/11/2026**

Trabajo Práctico Integrador – Programación II – UTN (Tecnicatura Universitaria en Programación a Distancia).

Sistema de consola en Python con Programación Orientada a Objetos: categorías, productos, usuarios y pedidos,
con inicio de sesión y menú según el rol (ADMIN / USUARIO). Los datos viven en memoria (colecciones).

**Integrantes:** Palazzolo López, Lucas Rubén – Dacrema, Maximiliano

**Docentes:** Tec. Rigoni Guerra, Cinthia – Tec. Enferrel, Ariel Edgardo · Facultad Regional Mendoza

## Cómo ejecutar

- Requisito: **Python 3.12 o superior** (probado en 3.13). Solo biblioteca estándar, no hay que instalar nada.
- Desde la carpeta del proyecto:

```bash
python main.py      # arranca el sistema
python pruebas.py   # pruebas del modelo y servicios (sin menú)
```

(En Windows, si `python` no funciona, probar `py main.py`.)

## Credenciales

| Rol | Mail | Contraseña |
|-----|------|-----------|
| ADMIN (administrador inicial) | `admin@foodstore.com` | `admin123` |
| USUARIO (cliente de ejemplo) | `juan@mail.com` | `juan123` |

Al iniciar, `main()` carga el administrador, un cliente y datos de ejemplo (4 categorías, 8 productos y un pedido).
Al cerrar el programa los datos se pierden (es lo esperado).

## Enlaces

- Video explicativo (10–15 min): [COMPLETAR: enlace con permisos públicos de visualización]
- Informe en PDF: [`TPI_FoodStore_Informe.pdf`](TPI_FoodStore_Informe.pdf) (subido a la raíz del repositorio y del .zip)
- Guion del video: `TPI_Guion_Palazzolo_Dacrema.pdf` (incluido en el .zip)
- Diagramas editables: `FoodStore_Diagramas.drawio` (abrir con diagrams.net / draw.io)
- Repositorio: [COMPLETAR: enlace de GitHub]

## Estructura (consola → servicios → entidades)

```
food_store/
├── main.py              # crea los servicios y arranca el menú principal (sin reglas de negocio)
├── pruebas.py           # pruebas del modelo y servicios, sin menú
├── entidades/           # Base (abstracta), Calculable (interfaz), Categoria, Producto, Usuario, Pedido, DetallePedido
├── enums/               # Rol, Estado, FormaPago
├── excepciones/         # FoodStoreError y subclases
├── servicios/           # CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio, datos iniciales
└── consola/             # Menu (abstracta), MenuAdministrador, MenuCliente, lectura validada, inicio de sesión
```

## Decisiones de diseño destacadas

- **Id por clase:** cada entidad tiene su propio contador (Categoria 1,2,3…; Producto 1,2,3…). `__eq__` compara clase e id.
- **Baja lógica:** `eliminar()` marca `eliminado = True`; el objeto sigue en la colección y no aparece en listados.
- **Creación de pedidos en 3 pasos:** `iniciar_pedido` → `agregar_item` (usa `Pedido.agregar_detalle`) → `confirmar_creacion`
  (usa `calcular_total()`, descuenta stock y recién ahí guarda). Si algo falla, no se guarda nada ni se toca el stock.
- **Producto "activo"** = no eliminado. Mail y nombre de categoría son únicos entre los no eliminados (el mail se guarda en minúsculas).
- **Reglas extra razonables:** un producto no disponible no se agrega a pedidos; un pedido TERMINADO/CANCELADO no admite
  cambios; un administrador no puede quitarse su propio rol estando en sesión.
- **Menús polimórficos:** `crear_menu()` es el único lugar donde se consulta el rol.
- La contraseña se guarda en memoria sin cifrar (alcance académico); un sistema real usaría un hash.

## Verificación realizada

`python pruebas.py` (106 comprobaciones, casos válidos y errores esperados), `mypy --strict` sin errores
y una prueba de entradas aleatorias sobre los menús sin ningún cierre inesperado.

## Funcionalidades

| Módulo | Administrador | Cliente (USUARIO) |
|--------|---------------|-------------------|
| Acceso | Login con mail y contraseña, 3 intentos, mensaje de error único | ídem |
| Categorías | Listar, crear, editar, eliminar (baja lógica) | Ver categorías |
| Productos | Listar, crear, editar, eliminar, listar por categoría | Ver productos disponibles |
| Usuarios | Listar, crear, editar, eliminar | Ver "Mis datos" |
| Pedidos | Listar todos, crear, cambiar estado y/o forma de pago, eliminar, listar por usuario, ver detalles | Ver "Mis pedidos" y su detalle |

### Menús

- **Administrador:** `1` Categorías · `2` Productos · `3` Usuarios · `4` Pedidos · `9` Cerrar sesión · `0` Salir.
  Cada submenú: `1` Listar · `2` Crear · `3` Editar · `4` Eliminar · `0` Volver (Productos suma `5` Listar por categoría; Pedidos
  suma `5` Listar por usuario y `6` Ver detalles, y su opción `3` es *Cambiar estado y/o forma de pago*).
- **Cliente:** `1` Ver categorías · `2` Ver productos disponibles · `3` Mis pedidos · `4` Mis datos · `9` Cerrar sesión · `0` Salir.
- Los enums se eligen por número (Estado: 1 PENDIENTE, 2 CONFIRMADO, 3 TERMINADO, 4 CANCELADO · Forma de pago: 1 TARJETA,
  2 TRANSFERENCIA, 3 EFECTIVO · Rol: 1 ADMIN, 2 USUARIO). Al editar, **Enter** conserva el valor actual.

## Reglas de negocio y validaciones

- Nombre de categoría y mail de usuario únicos (sin distinguir mayúsculas); no se elimina una categoría con productos activos.
- Precio no negativo, stock no negativo, cantidad mayor a 0; un producto no disponible no se puede pedir.
- Stock insuficiente: la creación del pedido se cancela completa (no se guarda el pedido ni se modifica el stock).
- Estados del pedido: PENDIENTE → CONFIRMADO → TERMINADO; PENDIENTE/CONFIRMADO → CANCELADO. TERMINADO y CANCELADO son finales.
  Al cancelar, el stock se devuelve.
- Un administrador no puede eliminarse a sí mismo. Cada cliente solo ve sus propios pedidos y datos.
- Edición "todo o nada": si un dato nuevo es inválido no se cambia ningún campo.

## Guía rápida para probar (recorrido sugerido)

1. `python main.py` → ingresar con `admin@foodstore.com` / `clave` (error) y luego con `admin123`.
2. Categorías → crear "Ensaladas"; probar duplicado "pizzas" y eliminar "Pizzas" (rechazado).
3. Productos → crear con precio `-500` (error) y luego válido; listar por categoría.
4. Usuarios → crear con el mail `juan@mail.com` (error: repetido).
5. Pedidos → crear para el usuario 2 con 2 Muzzarella + 1 Hamburguesa; crear otro con 5 Tiramisú (**stock insuficiente**, id 7 tiene stock 2).
6. Pedidos → cambiar estado PENDIENTE → TERMINADO (error); CONFIRMADO; CANCELADO (el stock se devuelve).
7. Cerrar sesión (`9`) e ingresar como `juan@mail.com` / `juan123`: ver el menú del cliente y sus pedidos.
8. Cerrar sesión y fallar 3 veces el login: el programa finaliza.

## Contenido de la entrega (.zip)

```
TPI_FoodStore_Entrega.zip
├── food_store/                       # código fuente completo (con este README.md en la raíz)
├── TPI_FoodStore_Informe.pdf         # informe (carátula, índice, marco teórico, arquitectura, capturas, dificultades, bibliografía)
├── FoodStore_Diagramas.drawio        # diagramas editables (draw.io / diagrams.net)
└── TPI_Guion_Palazzolo_Dacrema.pdf   # guion del video
```

## Correspondencia con la consigna

- POO: clase abstracta `Base` y `Menu`, interfaz `Calculable`, herencia, polimorfismo (menús por rol), encapsulamiento
  (propiedades, contraseña de solo escritura), composición Pedido–DetallePedido, agregación Categoría–Producto.
- Excepciones propias bajo `FoodStoreError`; colecciones (listas y diccionarios); type hints verificados con `mypy --strict`.
- Arquitectura en capas: consola → servicios → entidades; `main.py` sin reglas de negocio.
- Historias de usuario de las épicas 0 a 4 cubiertas (acceso, categorías, productos, usuarios, pedidos y detalles).

## Autores

Palazzolo López, Lucas Rubén · Dacrema, Maximiliano — Tec. Rigoni Guerra, Cinthia · Tec. Enferrel, Ariel Edgardo.
