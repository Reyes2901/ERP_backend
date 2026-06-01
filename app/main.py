from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.clientes import routes as clientes_routes
from app.inventario import routes as inventario_routes
from app.compras import routes as compras_routes
from app.ventas import routes as ventas_routes
from mangum import Mangum

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="ERP Backend para Mobile e IA Local. La lógica de negocio está completamente centralizada aquí.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CONFIGURACIÓN DE CORS CORREGIDA PARA APK
# Forzamos el ["*"] directamente en el middleware para evitar conflictos con la lista de orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # CRÍTICO: Esto permite que la APK conecte sin importar el protocolo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de los módulos (Sin cambios aquí)
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

# BLOQUE DE ARRANQUE OBLIGATORIO PARA RED LOCAL
if __name__ == "__main__":
    import uvicorn
    # Escucha en 0.0.0.0 para que la IP 192.168.0.9 sea accesible desde la APK
    uvicorn.run(app, host="0.0.0.0", port=8000)


#
handler = Mangum(app)