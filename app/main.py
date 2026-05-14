from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.clientes import routes as clientes_routes
from app.inventario import routes as inventario_routes
from app.compras import routes as compras_routes
from app.ventas import routes as ventas_routes

# Crear tablas en la base de datos (solo para desarrollo, en producción usar Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="ERP Backend para Mobile e IA Local. La lógica de negocio está completamente centralizada aquí.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS (permite conexiones desde Flutter y IA local)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000", # Para posible frontend web
    "*" # Permisivo para desarrollo, en producción restringir a tus dominios.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de los módulos
app.include_router(clientes_routes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(inventario_routes.router, prefix="/api/inventario", tags=["Inventario"])
app.include_router(compras_routes.router, prefix="/api/compras", tags=["Compras"])
app.include_router(ventas_routes.router, prefix="/api/ventas", tags=["Ventas"])

@app.get("/", tags=["Root"])
async def root():
    return {"success": True, "message": f"{settings.app_name} is running. Use /docs for API documentation."}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}