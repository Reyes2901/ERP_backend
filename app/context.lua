Actúa como un Arquitecto Senior Backend especializado en ERP, FastAPI, PostgreSQL y microservicios.

Necesito generar un ERP backend profesional en Python usando FastAPI y PostgreSQL.

# OBJETIVO GENERAL

Construir un ERP moderno orientado a mobile + IA local.

El ERP será consumido por:
- una app Flutter mobile
- un sistema IA local con Gemma GGUF + llama.cpp

La IA NO realizará lógica de negocio.
La IA solo enviará JSON estructurado.

Toda la lógica empresarial debe vivir en el backend FastAPI.

--------------------------------------------------
# ARQUITECTURA GENERAL
--------------------------------------------------

El proyecto debe usar arquitectura modular tipo microservicios simplificados.

Módulos principales:

1. clientes
2. inventario
3. compras
4. ventas

Cada módulo debe tener:
- routes
- services
- schemas
- models
- repositories

Arquitectura limpia y escalable.

--------------------------------------------------
# STACK TECNOLÓGICO
--------------------------------------------------

Usar:

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- Alembic
- Docker
- Docker Compose
- Uvicorn
- python-dotenv

--------------------------------------------------
# ESTRUCTURA DEL PROYECTO
--------------------------------------------------

Generar esta estructura:

erp_backend/
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── alembic/
│
├── app/
│   │
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   │
│   ├── clientes/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── inventario/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── compras/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── ventas/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   └── shared/
│       ├── exceptions.py
│       ├── responses.py
│       └── utils.py
│
└── tests/
    ├── clientes/
    ├── inventario/
    ├── compras/
    └── ventas/

--------------------------------------------------
# BASE DE DATOS
--------------------------------------------------

Usar PostgreSQL.

Configuración por variables de entorno.

Crear conexión profesional SQLAlchemy.

Usar:
- SessionLocal
- declarative_base
- dependency injection
- manejo correcto de sesiones

--------------------------------------------------
# MÓDULO CLIENTES
--------------------------------------------------

Tabla:
clientes

Campos:
- id
- nombre
- telefono
- email
- direccion
- created_at

Funcionalidades:
- crear cliente
- listar clientes
- obtener cliente por id
- actualizar cliente
- eliminar cliente

Validaciones:
- email único
- nombre obligatorio

Endpoints:
GET /clientes
GET /clientes/{id}
POST /clientes
PUT /clientes/{id}
DELETE /clientes/{id}

--------------------------------------------------
# MÓDULO INVENTARIO
--------------------------------------------------

Tabla:
productos

Campos:
- id
- nombre
- descripcion
- precio
- stock
- categoria
- created_at

Funcionalidades:
- crear producto
- listar productos
- actualizar stock
- eliminar producto
- buscar productos

Endpoints:
GET /inventario
GET /inventario/{id}
POST /inventario
PUT /inventario/{id}
DELETE /inventario/{id}

Reglas:
- stock nunca negativo
- precio mayor a 0

--------------------------------------------------
# MÓDULO COMPRAS
--------------------------------------------------

Debe existir:

Tabla:
compras

Campos:
- id
- proveedor
- total
- created_at

Tabla:
detalle_compras

Campos:
- id
- compra_id
- producto_id
- cantidad
- precio_unitario
- subtotal

Relaciones:
- una compra tiene múltiples detalles
- un producto puede estar en múltiples compras

Funcionalidades:
- registrar compra
- calcular total automáticamente
- aumentar stock automáticamente
- listar compras
- obtener compra detallada

Endpoints:
GET /compras
GET /compras/{id}
POST /compras

Lógica:
- el backend calcula subtotales
- el backend calcula total
- el backend actualiza inventario

--------------------------------------------------
# MÓDULO VENTAS
--------------------------------------------------

Debe existir:

Tabla:
ventas

Campos:
- id
- cliente_id
- total
- created_at

Tabla:
detalle_ventas

Campos:
- id
- venta_id
- producto_id
- cantidad
- precio_unitario
- subtotal

Relaciones:
- una venta tiene múltiples productos
- un cliente tiene múltiples ventas

Funcionalidades:
- registrar venta
- validar stock disponible
- descontar stock automáticamente
- calcular total automáticamente
- listar ventas
- obtener venta detallada

Endpoints:
GET /ventas
GET /ventas/{id}
POST /ventas

REGLAS IMPORTANTES:
- NO permitir stock negativo
- NO confiar en cálculos enviados desde frontend
- el backend debe calcular todo
- usar transacciones SQLAlchemy

--------------------------------------------------
# RELACIONES ORM
--------------------------------------------------

Usar SQLAlchemy relationships correctamente:

- Cliente -> ventas
- Venta -> detalle_ventas
- Producto -> detalle_ventas
- Compra -> detalle_compras
- Producto -> detalle_compras

Usar:
- back_populates
- cascade delete
- lazy loading

--------------------------------------------------
# SCHEMAS PYDANTIC
--------------------------------------------------

Generar:
- Create schemas
- Update schemas
- Response schemas

Usar:
- validaciones
- tipos correctos
- Field()
- EmailStr
- Config orm_mode

--------------------------------------------------
# SERVICES
--------------------------------------------------

Toda la lógica de negocio debe estar en services.py

NO poner lógica en routes.py

Ejemplos:
- calcular total venta
- validar stock
- actualizar inventario
- crear detalle ventas
- calcular compras

--------------------------------------------------
# REPOSITORIES
--------------------------------------------------

Repositories deben manejar:
- queries SQLAlchemy
- acceso DB
- filtros
- búsquedas

Separar claramente:
routes -> services -> repositories

--------------------------------------------------
# RESPUESTAS API
--------------------------------------------------

Usar respuestas JSON consistentes:

{
  "success": true,
  "message": "Venta registrada",
  "data": {}
}

Manejo profesional de errores:
- 404
- 400
- 422
- 500

--------------------------------------------------
# DOCUMENTACIÓN
--------------------------------------------------

FastAPI Swagger automático:

/docs

Agregar:
- tags
- summaries
- descriptions

--------------------------------------------------
# DOCKER
--------------------------------------------------

Crear:
- Dockerfile
- docker-compose.yml

Docker Compose debe levantar:
- backend FastAPI
- PostgreSQL

Variables:
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

--------------------------------------------------
# SEGURIDAD
--------------------------------------------------

Preparar estructura para:
- JWT
- autenticación futura
- middleware
- CORS

Aunque inicialmente no implementar login completo.

--------------------------------------------------
# PREPARADO PARA IA
--------------------------------------------------

El backend será consumido por una IA local.

La IA enviará JSON como:

{
  "module": "ventas",
  "action": "create",
  "cliente_id": 1,
  "productos": [
    {
      "producto_id": 2,
      "cantidad": 3
    }
  ]
}

El backend debe:
- validar datos
- calcular precios
- calcular totales
- actualizar stock

La IA NO debe realizar cálculos financieros.

--------------------------------------------------
# TESTING
--------------------------------------------------

Generar ejemplos de:
- pytest
- tests endpoints
- tests services

--------------------------------------------------
# RESULTADO ESPERADO
--------------------------------------------------

Generar:
- código completo
- estructura completa
- modelos
- schemas
- services
- repositories
- rutas
- Docker
- PostgreSQL
- ejemplos funcionales
- buenas prácticas profesionales

El código debe estar listo para ejecutar en producción y conectarse posteriormente a Flutter Mobile y a un sistema IA local.